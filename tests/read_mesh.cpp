#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <sys/stat.h>

#include "KDTree.hpp"
#include "opencv2/opencv.hpp"

std::vector<std::string> split(std::string line, char delimiter) {
  std::vector<std::string> answer;
  std::stringstream ss(line);
  std::string temp;

  while (std::getline(ss, temp, delimiter)) {
      answer.push_back(temp);
  }

  return answer;
}

cv::Mat homographyMat(pointVec &pt){
    // Four corners of the book in source image
    std::vector<cv::Point2f> pts_src;
    pts_src.push_back(cv::Point2f(pt[0][1], pt[0][2]));
    pts_src.push_back(cv::Point2f(pt[1][1], pt[1][2]));
    pts_src.push_back(cv::Point2f(pt[2][1], pt[2][2]));
    pts_src.push_back(cv::Point2f(pt[3][1], pt[3][2]));

    // Four corners of the book in destination image.
    std::vector<cv::Point2f> pts_dst;
    pts_dst.push_back(cv::Point2f(0, 0));
    pts_dst.push_back(cv::Point2f(1, 0));
    pts_dst.push_back(cv::Point2f(1, 1));
    pts_dst.push_back(cv::Point2f(0, 1));

    // Calculate Homography
    cv::Mat h = cv::findHomography(pts_src, pts_dst);

    for(int j = 0; j < 4; j++){
      point_t pt_p;
      std::cout << "homography h checking: ";
      for(int i = 0; i < 2; i++){
          pt_p.push_back(h.at<double>(i,0)*pt[j][1]+h.at<double>(i,1)*pt[j][2]+h.at<double>(i,2));
      }
      std::cout << pt_p[0] << " " << pt_p[1] << std::endl;
    }  

    return h;
}

// read the mesh file and save the vertices and vertex normals 1-to-1
std::tuple<pointVec, pointVec, double, double,double,double> readMesh (const std::string file_name) {
  pointVec points;
  pointVec normals;
  pointVec vns;

  point_t pt;
  point_t n;

  double min_y=10000, max_y=-100000;
  double min_z=10000, max_z=-100000;

  bool assigned = false;

  // read file
  std::ifstream infile(file_name);
  std::string line_;  // line read
  while (std::getline(infile, line_))
  {
    std::vector<std::string> line = split(line_, ' ');  // splitted line
    if (line[0] == "v") { // vertex
      pt = {std::stod(line[1]), std::stod(line[2]), std::stod(line[3])};
      points.push_back(pt);
      if(std::stod(line[2]) < min_y) min_y = std::stod(line[2]);
      else if (std::stod(line[2]) > max_y) max_y = std::stod(line[2]);
      if(std::stod(line[3]) < min_z) min_z = std::stod(line[3]);
      else if (std::stod(line[3]) > max_z) max_z = std::stod(line[3]);
    }
    else if (line[0] == "vn") { // vertex normal
      n = {std::stod(line[1]), std::stod(line[2]), std::stod(line[3])};
      vns.push_back(n);
    }
    if (line[0] == "f") { // face
      if (!assigned) {  // assign vector
        normals.assign(points.size(), point_t(3, 0.0));
        assigned = true;
      }
      line.erase(line.begin()); // erase f
      for (auto element: line) {
        std::vector<std::string> vvn = split(element, '/');
        int v_index = std::stoi(vvn[0])-1;
        int vn_index = std::stoi(vvn[2])-1;
        normals[v_index] = vns[vn_index];
      }
    }
  }
  return {points, normals, min_y, max_y, min_z, max_z};
}

int main() {
  pointVec points;
  pointVec normals;
  double min_y, max_y, min_z, max_z;

  // read mesh file
  std::string file_name = "../input/bee_hive_2_face.obj"; // assume that file is executed in /build folder
  struct stat buffer;   
  if(stat (file_name.c_str(), &buffer) != 0){
    std::cout << "FILE NOT FOUND\n";
    return 0;
  };

  tie(points, normals, min_y, max_y, min_z, max_z) = readMesh(file_name);

  // transform points so that the wall would have drawings (0,0) coordinate on the middle
  std::cout << "Min and Max Y: " << min_y << " " << max_y << std::endl;
  std::cout << "Min and Max Z: " << min_z << " " << max_z << std::endl;
  double mid_y = (max_y+min_y)/2;
  double mid_z = (max_z+min_z)/2;
  // for(int i = 0; i < points.size(); i++) {
  //   points[i][1] -= mid_y;
  //   points[i][2] -= mid_z;
  // }

  // make KDTree
  KDTree tree(points, normals);

  // print out the points and normals
  // for (size_t i = 0 ; i < points.size() ; i ++) {
  //   std::cout << i << "th :" ;
  //   std::cout << "point :" << points[i][0] << ", " << points[i][1] << ", " << points[i][2] << std::endl;
  //   std::cout << "normal :" << normals[i][0] << ", " << normals[i][1] << ", " << normals[i][2] << std::endl;
  // }

  // tree.print_tree();

  point_t pt = {-0.9, 0.4};

  // std::cout << "\nnearest test\n";
  // auto res = tree.nearest_point(pt);
  // for (double b : res) {
  //   std::cout << b << " ";
  // }

  std::cout << "\n\nneighborhood\n";
  auto res2 = tree.neighborhood_points(pt, 2);
  std::cout << res2.size() << std::endl;
  // for (point_t a : res2) {
  //     for (double b : a) {
  //         std::cout << b << " ";
  //     }
  //     std::cout << '\n';
  // }

  std::cout << "\nNearest 4 points\n";
  auto res3 = tree.search_quad(pt, 2);
  for (auto a : res3) {
    point_t pt = a->xyz();
    std::cout << pt[0] << ", " << pt[1] << ", " << pt[2]<< '\n';
  }

  pointVec coor = {res3[0]->xyz(), res3[1]->xyz(), res3[2]->xyz(), res3[3]->xyz()};
  pointVec nv = {res3[0]->n, res3[1]->n, res3[2]->n, res3[3]->n};
      
  // matrix to convert quad to rectangle 
  cv::Mat h = homographyMat(coor);  // 3X3 matrix
  // cv::Mat h_Inv=h.inv();

  // bilinear interpolation
  point_t pt_p;
  for(int i = 0; i < 3; i++){
      pt_p.push_back(h.at<double>(i,0)*pt[1]+h.at<double>(i,1)*pt[2]+h.at<double>(i,2));
  }

  double dy = 1-pt_p[0];
  double dz = pt_p[1];

  double A = dy*(1-dz);
  double B = (1-dy)*(1-dz);
  double C = (1-dy)*(dz);
  double D = dy*(dz);

  point_t normal_vector;
  double x_ = A*coor[0][0]+B*coor[1][0]+C*coor[2][0]+D*coor[3][0];
  for(int i = 0; i < 3; i++){
    normal_vector.push_back(A*nv[0][i]+B*nv[1][i]+C*nv[2][i]+D*nv[3][i]);
  }

  std::cout << "normal vector: " << normal_vector[0] << ", " << normal_vector[1] << ", " << normal_vector[2] << std::endl;
  std::cout << "x: " << x_ << std::endl;

  return 0;
}
