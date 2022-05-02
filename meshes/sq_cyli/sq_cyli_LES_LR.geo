// Gmsh project created on Thu Oct 28 18:18:28 2021
SetFactory("OpenCASCADE");

// Square cylinder
//Rectangle(1) = {-0.5, -0.5, 0, 1, 1, 0};

// Constants
xinlet = -10.5;
xoutlet = 20;
xcyli = -0.5;
dx = 1;
yinlet = 0.5;
ybound = 27;
ycyli = 0.5;

// Points
Point(1) = {xcyli, -ycyli, 0, 1.0};
Point(2) = {xcyli+dx, -ycyli, 0, 1.0};
Point(3) = {xcyli+dx, ycyli, 0, 1.0};
Point(4) = {xcyli, ycyli, 0, 1.0};
Point(5) = {xinlet, ybound, 0, 1.0};
Point(6) = {xinlet, -ybound, 0, 1.0};
Point(7) = {xinlet, yinlet, 0, 1.0};
Point(8) = {xinlet, -yinlet, 0, 1.0};
Point(9) = {xcyli, ybound, 0, 1.0};
Point(10) = {xcyli, -ybound, 0, 1.0};
Point(11) = {xcyli+dx, ybound, 0, 1.0};
Point(12) = {xcyli+dx, -ybound, 0, 1.0};
Point(13) = {xoutlet, ybound, 0, 1.0};
Point(14) = {xoutlet, -ybound, 0, 1.0};
Point(15) = {xoutlet, yinlet, 0, 1.0};
Point(16) = {xoutlet, -yinlet, 0, 1.0};

// Lines
Line(5) = {5, 9};
Line(6) = {6, 10};
Line(7) = {7, 4};
Line(8) = {8, 1};
Line(9) = {9, 11};
Line(10) = {10, 12};
Line(11) = {11, 13};
Line(12) = {12, 14};
Line(13) = {3, 15};
Line(14) = {2, 16};
Line(15) = {5, 7};
Line(16) = {6, 8};
Line(17) = {7, 8};
Line(18) = {9, 4};
Line(19) = {10, 1};
Line(20) = {11, 3};
Line(21) = {12, 2};
Line(22) = {13, 15};
Line(23) = {14, 16};
Line(24) = {15, 16};
Line(25) = {4, 3};
Line(26) = {1, 2};
Line(27) = {4, 1};
Line(28) = {3, 2};

// Define number of nodes
xncyli = 120;
xnfar = 80;
yncyli = xncyli;
yninlet = 60;
ynoutlet = 55;
// Transfinite lines
Transfinite Curve {9, 10, 25, 26} = yncyli Using Bump 0.0001;
Transfinite Curve {17, 24, 27, 28} = xncyli Using Bump 0.0001;
Transfinite Curve {15, 16, 18, 19, 20, 21, 22, 23} = xnfar Using Progression 0.84;
Transfinite Curve {5, 6, 7, 8} = yninlet Using Progression 0.80;
Transfinite Curve {11, 12, 13, 14} = ynoutlet Using Progression 1.297;
// x: 480; y: 330
// Define plane surfaces
Curve Loop(1) = {7, -18, -5, 15};
Plane Surface(1) = {1};
Curve Loop(2) = {18, 25, -20, -9};
Plane Surface(2) = {2};
Curve Loop(3) = {20, 13, -22, -11};
Plane Surface(3) = {3};
Curve Loop(4) = {28, 14, -24, -13};
Plane Surface(4) = {4};
Curve Loop(5) = {21, 14, -23, -12};
Plane Surface(5) = {5};
Curve Loop(6) = {19, 26, -21, -10};
Plane Surface(6) = {6};
Curve Loop(7) = {16, 8, -19, -6};
Plane Surface(7) = {7};
Curve Loop(8) = {17, 8, -27, -7};
Plane Surface(8) = {8};

// Transfinite surfaces and recombine them
Transfinite Surface {1};
Transfinite Surface {2};
Transfinite Surface {3};
Transfinite Surface {4};
Transfinite Surface {5};
Transfinite Surface {6};
Transfinite Surface {7};
Transfinite Surface {8};

Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8};
// Extrude 1 unit to make it runable on OpenFOAM
Extrude {0, 0, 1} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{5}; Surface{6}; Surface{7}; Surface{8}; Layers{80}; Recombine;
}
// Define physical volumes and surfaces
Physical Volume("Fluid") = {1, 2, 3, 4, 5, 6, 7, 8};
//Physical Surface("Inlet") = {12, 34, 38, 36, 28, 32, 11, 16, 20};
Physical Surface("Inlet") = {12, 34, 38};
Physical Surface("Outlet") = {19, 24, 27};
Physical Surface("OutletSide1") = {11, 16, 20};
Physical Surface("OutletSide2") = {36, 32, 28};
Physical Surface("Cylinder") = {39, 14, 22, 31};
//Physical Surface("Side") = {21, 17, 13, 40, 37, 25, 33, 29, 7, 6, 5, 8, 1, 4, 3, 2};
Physical Surface("TopSide") = {13, 17, 21, 40, 25, 29, 33, 37};
Physical Surface("BotSide") = {2, 7, 6, 5, 4, 3, 1, 8};
