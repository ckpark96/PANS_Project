// Define constants for points
dx = 1; // length of square cylinder
dy = dx;
dx2 = 4; // length of inner square
dy2 = dx2;
xinlet = -8;
yfar = 7;
ynear = dy2/2;
xnear = dx2/2;
xfar = 20;
yinletdev = 1.5;
youtletdev = 2.5;
xdev = 1.5;
/////////// POINTS
// Define points around square cylinder
Point(1) = {-dx/2, dy/2, 0, 1.0};
Point(2) = {-dx/2, -dy/2, 0, 1.0};
Point(3) = {dx/2, -dy/2, 0, 1.0};
Point(4) = {dx/2, dy/2, 0, 1.0};
// Define poitns around the inner square
Point(5) = {-xnear, ynear, 0, 1.0};
Point(6) = {-xnear, -ynear, 0, 1.0};
Point(7) = {xnear, -ynear, 0, 1.0};
Point(8) = {xnear, ynear, 0, 1.0};
// Define the points surrounding domain
Point(9) = {xinlet, yfar, 0, 1.0};
Point(10) = {xinlet, ynear+yinletdev, 0, 1.0};
Point(11) = {xinlet, -ynear-yinletdev, 0, 1.0};
Point(12) = {xinlet, -yfar, 0, 1.0};
Point(13) = {-xnear-xdev, -yfar, 0, 1.0};
Point(14) = {xnear+xdev, -yfar, 0, 1.0};
Point(15) = {xfar, -yfar, 0, 1.0};
Point(16) = {xfar, -ynear-youtletdev, 0, 1.0};
Point(17) = {xfar, ynear+youtletdev, 0, 1.0};
Point(18) = {xfar, yfar, 0, 1.0};
Point(19) = {xnear+xdev, yfar, 0, 1.0};
Point(20) = {-xnear-xdev, yfar, 0, 1.0};
////////// LINES
// Diagonal lines inside inner square
Line(1) = {5, 1};
Line(2) = {6, 2};
Line(3) = {7, 3};
Line(4) = {8, 4};
// Vertical lines in the middle
Line(5) = {11, 10};
Line(6) = {6, 5};
Line(7) = {2, 1};
Line(8) = {3, 4};
Line(9) = {7, 8};
Line(10) = {16, 17};
// Horizontal lines in the 'middle'
Line(11) = {13, 14};
Line(12) = {6, 7};
Line(13) = {2, 3};
Line(14) = {1, 4};
Line(15) = {5, 8};
Line(16) = {20, 19};
// Outer vertical lines
Line(17) = {9, 10};
Line(18) = {12, 11};
Line(19) = {20, 5};
Line(20) = {13, 6};
Line(21) = {19, 8};
Line(22) = {14, 7};
Line(23) = {18, 17};
Line(24) = {15, 16};
// Inlet horizontal lines
Line(25) = {12, 13};
Line(26) = {11, 6};
Line(27) = {10, 5};
Line(28) = {9, 20};
// Outlet horizontal lines
Line(29) = {15, 14};
Line(30) = {16, 7};
Line(31) = {17, 8};
Line(32) = {18, 19};
//////////// TRANSFINITE
ndiag = 135;
nymid = 200;
nxmid = nymid;
nyfar = 35;
nxinlet = 40;
nxoutlet = 70;
// Diagonal lines inside inner square
Transfinite Curve {1,2,3,4} = ndiag Using Progression 0.94;
// Vertical lines in the middle
Transfinite Curve {7,8,10} = nymid Using Progression 1;
// Horizontal lines in the 'middle'
Transfinite Curve {11,13,14,16} = nxmid Using Progression 1;
// Perimeters of inner circle
Transfinite Curve {6,9,12,15} = nxmid Using Bump 18;
// Lines outside the 'cross'
Transfinite Curve {5} = nymid Using Bump 5; // left
Transfinite Curve {10} = nymid Using Bump 1.5; // right
Transfinite Curve {11,16} = nxmid Using Bump 10; // bottom and top
// Outer vertical lines
Transfinite Curve {17,18,19,20,21,22,23,24} = nyfar Using Progression 0.98;
// Inlet horizontal lines
Transfinite Curve {26,27} = nxinlet Using Progression 0.975;
Transfinite Curve {25,28} = nxinlet Using Progression 1;
// Outlet horizontal lines
Transfinite Curve {30,31} = nxoutlet Using Progression 0.975;
Transfinite Curve {29,32} = nxoutlet Using Progression 0.985;
/////// SURFACES
Curve Loop(1) = {1, -7, -2, 6};
Plane Surface(1) = {1};
Curve Loop(2) = {2, 13, -3, -12};
Plane Surface(2) = {2};
Curve Loop(3) = {8, -4, -9, 3};
Plane Surface(3) = {3};
Curve Loop(4) = {4, -14, -1, 15};
Plane Surface(4) = {4};
Curve Loop(5) = {28, 19, -27, -17};
Plane Surface(5) = {5};
Curve Loop(6) = {27, -6, -26, 5};
Plane Surface(6) = {6};
Curve Loop(7) = {26, -20, -25, 18};
Plane Surface(7) = {7};
Curve Loop(8) = {20, 12, -22, -11};
Plane Surface(8) = {8};
Curve Loop(9) = {22, -30, -24, 29};
Plane Surface(9) = {9};
Curve Loop(10) = {9, -31, -10, 30};
Plane Surface(10) = {10};
Curve Loop(11) = {31, -21, -32, 23};
Plane Surface(11) = {11};
Curve Loop(12) = {21, -15, -19, 16};
Plane Surface(12) = {12};
////// TRANSFINITE SURFACES
Transfinite Surface {1};
Transfinite Surface {2};
Transfinite Surface {3};
Transfinite Surface {4};
Transfinite Surface {5};
Transfinite Surface {6};
Transfinite Surface {7};
Transfinite Surface {8};
Transfinite Surface {9};
Transfinite Surface {10};
Transfinite Surface {11};
Transfinite Surface {12};
////// RECOMBINE SURFACES
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
////// EXTRUDE SURFACES
Extrude {0, 0, 1} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Layers{1}; Recombine;
}
///// DEFINE PHYSICAL GROUP
Physical Surface("Inlet") = {141, 163, 185, 269, 295, 129, 181, 207, 229};
Physical Surface("Outlet") = {273, 247, 225};
Physical Surface("Cylinder") = {111, 85, 67, 45};
Physical Surface("Side") = {142, 5, 12, 296, 6, 164, 7, 186, 8, 208, 9, 230, 10, 252, 11, 274, 120, 4, 98, 3, 76, 2, 54, 1};
Physical Volume("Fluid") = {5, 6, 7, 12, 8, 9, 10, 11, 2, 3, 4, 1};
