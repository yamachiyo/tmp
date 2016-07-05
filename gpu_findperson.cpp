#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <opencv2/opencv.hpp>
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "ros/ros.h"
#include "std_msgs/Int32.h"

using namespace cv;
using namespace cv::ml;
using namespace std;

void get_svm_detector(const Ptr<SVM>& svm, vector< float > & hog_detector );
void get_svm_detector(const Ptr<SVM>& svm, vector< float > & hog_detector )
{
    // get the support vectors
    Mat sv = svm->getSupportVectors();
    const int sv_total = sv.rows;
    // get the decision function
    Mat alpha, svidx;
    double rho = svm->getDecisionFunction(0, alpha, svidx);

    CV_Assert( alpha.total() == 1 && svidx.total() == 1 && sv_total == 1 );
    CV_Assert( (alpha.type() == CV_64F && alpha.at<double>(0) == 1.) ||
               (alpha.type() == CV_32F && alpha.at<float>(0) == 1.f) );
    CV_Assert( sv.type() == CV_32F );
    hog_detector.clear();

    hog_detector.resize(sv.cols + 1);
    memcpy(&hog_detector[0], sv.ptr(), sv.cols*sizeof(hog_detector[0]));
    hog_detector[sv.cols] = (float)-rho;
}


int
main(int argc, char *argv[])
{
  //ROS
  ros::init(argc, argv, "findperson");
  ros::NodeHandle n;
  ros::Publisher fp_pub = n.advertise<std_msgs::Int32>("camera_fp", 3);
  ros::Rate loop_rate(10);
  std_msgs::Int32 person_x;

  cv::VideoCapture cap(0);
  if(!cap.isOpened()) return -1;
  
  //load svm
  svm = cv::ml::StatModel::load<SVM>("my_people_detector.yml");
  std::vector<float> hog_detector;
  get_svm_detector( svm, hog_detector );

  cv::gpu::HOGDescriptor hog;
  //hog.setSVMDetector(cv::gpu::HOGDescriptor::getDefaultPeopleDetector());
  hog.setSVMDetector(hog_detector);

  cv::Mat img;
  cv::Mat gray_img;
  cv::gpu::GpuMat gpu_img;

  while(ros::ok())
  {
    person_x.data = 0;

    cap >> img;
    cv::cvtColor(img, gray_img, CV_BGR2GRAY);
    gpu_img.upload(gray_img);

    std::vector<cv::Rect> found;

    hog.detectMultiScale(gpu_img, found, 0., cv::Size(8,8), cv::Size(0,0), 1.15, 2);

    std::cout << "found:" << found.size() << std::endl;
    for(size_t i = 0; i < found.size(); i++) {
      cv::Rect r = found[i];
      cv::rectangle(img, r.tl(), r.br(), cv::Scalar(255,0,0), 2);
      std::cout << found[i] << std::endl;
    }

    // 結果の描画
    cv::namedWindow("result", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
    cv::imshow( "result", img );    
    cv::waitKey(1);

    //publish a NEAREST Rect center_x
    int data_x;
    cv::Rect data_n;

    if(found.size() == 1) {
      data_x = (found[0].tl().x + found[0].br().x)/2 ;

      person_x.data = data_x ;
    }

    if(found.size() > 1) {
      data_n = found[0];
      for(size_t i = 1; i < found.size(); i++) {
        if(data_n.br().y < found[i].br().y) data_n = found[i];
      }
      data_x = (data_n.tl().x + data_n.br().x)/2 ;

      person_x.data = data_x ;
    }

    if(found.size() == 0) {
      person_x.data = -1 ;
    }

    fp_pub.publish(person_x);
    std::cout << "send data:" << person_x.data << std::endl;

    ros::spinOnce();
    loop_rate.sleep();
  }
}
