#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>

int
main(int argc, char *argv[])
{
  cv::VideoCapture cap(0);
  if(!cap.isOpened()) return -1;
  
  cv::gpu::HOGDescriptor hog;
  hog.setSVMDetector(cv::gpu::HOGDescriptor::getDefaultPeopleDetector());

  cv::Mat img;
  cv::Mat gray_img;
  cv::gpu::GpuMat gpu_img;

  while(true)
  {
    cap >> img;
    cv::cvtColor(img, gray_img, CV_BGR2GRAY);
    gpu_img.upload(gray_img);

    std::vector<cv::Rect> found;

    hog.detectMultiScale(gpu_img, found, 0., cv::Size(8,8), cv::Size(0,0), 1.15, 2);

    std::vector<cv::Rect>::const_iterator it = found.begin();
    std::cout << "found:" << found.size() << std::endl;
    for(size_t i = 0; i < found.size(); i++) {
      cv::Rect r = found[i];
      cv::rectangle(img, r.tl(), r.br(), cv::Scalar(255,0,0), 2);
    }

    // 結果の描画
    cv::namedWindow("result", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
    cv::imshow( "result", img );    
    int key = cv::waitKey(1);
    if(key > 0) break;
  }
}
