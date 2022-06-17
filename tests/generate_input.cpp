#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <sys/stat.h>

#include "KDTree.hpp"
#include "opencv2/opencv.hpp"

#define TARGET_SIZE    0.1
#define TRANSLATE_UP   1.0
#define WALL_OBJ "../../input/half_sphere_out.obj"
#define DRAWING_TXT "../../input/grid_fix.txt"
#define OUTPUT_TXT "../../output/grid.txt"

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

    return h;
}

// read the mesh file and save the vertices and vertex normals 1-to-1
std::tuple<pointVec, pointVec, double, double,double,double> readMesh (const std::string wall_name) {
  pointVec points;
  pointVec normals;
  pointVec vns;
  pointVec uvs;

  point_t pt;
  point_t uv;
  point_t n;

  double min_y=10000, max_y=-100000;
  double min_z=10000, max_z=-100000;

  bool assigned = false;

  // read file
  std::ifstream infile(wall_name);
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
    else if (line[0] == "vt") { // parameterized vertex (u,v)
      uv = {std::stod(line[1]), std::stod(line[2]), std::stod(line[3])};
      uvs.push_back(n);
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

  // Make y = 0 as the center of the wall coordinate and z = 0 as the bottom of the wall
  double mid_y = (min_y+max_y)/2;
  for(int i = 0; i < points.size(); i++){
    points[i][1] += - mid_y;
    points[i][2] += - min_z;
  }
  return {points, uvs, normals, min_y, max_y, min_z, max_z};
}

int main() {
  pointVec points, uvs, normals;
  double min_y, max_y, min_z, max_z;

  // read mesh file
  std::string mesh_name = WALL_OBJ; // assume that file is executed in /build folder
  struct stat buffer;   
  if(stat (mesh_name.c_str(), &buffer) != 0){
    std::cout << "FILE NOT FOUND\n";
    return 0;
  };

  tie(points, uvs normals, min_y, max_y, min_z, max_z) = readMesh(mesh_name);

  // transform points so that the wall would have drawings (0,0) coordinate on the middle
  //std::cout << "Min and Max Y: " << min_y << " " << max_y << std::endl;
  //std::cout << "Min and Max Z: " << min_z << " " << max_z << std::endl;
  //double mid_y = (max_y+min_y)/2;
  //double mid_z = (max_z+min_z)/2;
  //for(int i = 0; i < points.size(); i++) {
  //  points[i][1] -= mid_y;
  //  points[i][2] -= mid_z;
  //}

  // make KDTree
  std::cout << "Create KD Tree\n";
  KDTree tree(points, uvs, normals);

  // tree.print_tree();

  // read drawing file
  std::string drawing_name = DRAWING_TXT; // assume that file is executed in /build folder
  if(stat (drawing_name.c_str(), &buffer) != 0){
    std::cout << "FILE NOT FOUND\n";
    return 0;
  };

  // read file
  std::ifstream infile(drawing_name);
  std::string output_name = OUTPUT_TXT;
  std::ofstream outfile(output_name);
  std::string line_;  // line read

  // ignore first line, which contains image size data
  std::getline(infile, line_); 
  std::vector<std::string> line = split(line_, ' ');  // splitted line
  double ratio = std::stod(line[0])/std::stod(line[1]);
  outfile << line_ << "\n";

  std::cout << "Convert Drawing File\n";
  while (std::getline(infile, line_)){
    if(line_ == "End") outfile << line_ << "\n";
    else{
      line = split(line_, ' ');  // splitted line
      point_t pt;
      pt.push_back(std::stod(line[0]*0.5+0.25);  // y
      pt.push_back(std::stod(line[1]*0.5+0.25); // z
      // std::cout << "drawing point: " << pt[0] << ", " << pt[1] << std::endl;

      // find the nearest point
      auto quad = tree.


      /*
      // std::cout << "\nNearest 4 points\n";
      auto quad = tree.search_quad(pt, 3);

      pointVec coor = {quad[0]->xyz(), quad[1]->xyz(), quad[2]->xyz(), quad[3]->xyz()};
      pointVec uv = {quad[0]->uv(), quad[1]->uv(), quad[2]->uv(), quad[3]->uv()};
      pointVec nv = {quad[0]->n, quad[1]->n, quad[2]->n, quad[3]->n};

      double dy = uv[1][1]-pt[0];
      double dz = uv[2][2]-pt[1];

      double A = (1-dy)*(1-dz);
      double B = dy*(1-dz);
      double C = (dy)*(dz);
      double D = (1-dy)*(dz);

      double fy1 = (coor[1][1]-pt[0])*coor[0][0] + (pt[0]-coor[0][1])*coor[1][0];
      fy1 = fy1/(coor[1][1]-coor[0][1]);
      double fy2 = (coor[1][1]-pt[0])*coor[3][0] + (pt[0]-coor[0][1])*coor[2][0];
      fy2 = fy2/(coor[1][1]-coor[0][1]);
      double x = (coor[3][2]-pt[1])*fy1 + (pt[1]-coor[0][2])*fy2;
      x = x/(coor[3][2]-coor[0][2]);

      point_t normal_vector;
      // double x = A*coor[0][0]+B*coor[1][0]+C*coor[2][0]+D*coor[3][0];
      for(int i = 0; i < 3; i++){
        normal_vector.push_back(A*nv[0][i]+B*nv[1][i]+C*nv[2][i]+D*nv[3][i]);
      }
      */



      if(x < -1.5){
        std::cout << "point: " << x << " " << pt[0] << " " << pt[1] << std::endl;
        std::cout << "normal: " << normal_vector[0] << " " << normal_vector[1] << " " << normal_vector[2] << std::endl;
        std::cout << "quad: \n" ;
        for(int i = 0; i < 4; i ++){
          std::cout << coor[i][0] << " " << coor[i][1] << " " << coor[i][2] << std::endl;
        }
        std::cout << std::endl;
      }
      else {
      // outfile << std::to_string(x) << " " << line[0] << " " << line[1] << "\n";
        outfile << std::to_string(x) << " " << std::to_string(pt[0]) << " " << std::to_string(pt[1]) << " " << std::to_string(normal_vector[0]) << " " << std::to_string(normal_vector[1]) << " " << std::to_string(normal_vector[2]) <<"\n";
      }

      // std::cout << "normal vector: " << normal_vector[0] << ", " << normal_vector[1] << ", " << normal_vector[2] << std::endl;
      // std::cout << "x: " << x_ << std::endl;
    }
  }
  return 0;
}
