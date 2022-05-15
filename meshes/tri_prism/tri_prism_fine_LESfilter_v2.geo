xinlet      = -0.01;
xinlet2     = -0.005;
xoutlet     = 0.3;
xtriFront   = 0;
xtriRear    = 0.034641;
xtriRear2   = 0.0435;
ynearTri    = 0.02;
ynearInlet1 = 0.031;
ynearInlet  = 0.03;
ynearTriTip = 0.035;
ynearOutlet = 0.035;
yfar        = 0.06;
//+
Point(1) = {xtriFront, 0, 0, 1.0};
Point(2) = {xtriRear, ynearTri, 0, 1.0};
Point(3) = {xtriRear, -ynearTri, 0, 1.0};

Point(4) = {xinlet, 0, 0, 1.0};
Point(5) = {xinlet, ynearInlet, 0, 1.0};
Point(6) = {xinlet, -ynearInlet, 0, 1.0};
Point(7) = {xinlet, yfar, 0, 1.0};
Point(8) = {xinlet, -yfar, 0, 1.0};

Point(9)  = {xinlet2, 0, 0, 1.0};
Point(10) = {xinlet2, ynearInlet, 0, 1.0};
Point(11) = {xinlet2, -ynearInlet, 0, 1.0};
Point(12) = {xinlet2, yfar, 0, 1.0};
Point(13) = {xinlet2, -yfar, 0, 1.0};

Point(14) = {xtriFront, ynearInlet1, 0, 1.0};
Point(15) = {xtriFront, -ynearInlet1, 0, 1.0};
Point(16) = {xtriFront, yfar, 0, 1.0};
Point(17) = {xtriFront, -yfar, 0, 1.0};

Point(18) = {xtriRear2, ynearOutlet, 0, 1.0};
Point(19) = {xtriRear2, -ynearOutlet, 0, 1.0};
Point(20) = {xtriRear2, yfar, 0, 1.0};
Point(21) = {xtriRear2, -yfar, 0, 1.0};

Point(22) = {xoutlet, ynearOutlet, 0, 1.0};
Point(23) = {xoutlet, -ynearOutlet, 0, 1.0};
Point(24) = {xoutlet, yfar, 0, 1.0};
Point(25) = {xoutlet, -yfar, 0, 1.0};
//+
// Lines go outside-inwards or bottom-up or left-right
// Horizontal lines
Line(1) = {1, 2};
Line(2) = {1, 3};
Line(3) = {3, 2};

Line(4) = {4, 9};
Line(5) = {5, 10};
Line(6) = {6, 11};
Line(7) = {7, 12};
Line(8) = {8, 13};

Line(9)  = {9, 1};
Line(10) = {10, 14};
Line(11) = {11, 15};
Line(12) = {12, 16};
Line(13) = {13, 17};

Line(14) = {18, 14};
Line(15) = {19, 15};
Line(16) = {18, 2};
Line(17) = {19, 3};
Line(18) = {16, 20};
Line(19) = {17, 21};

Line(20) = {22, 18};
Line(21) = {23, 19};
Line(22) = {24, 20};
Line(23) = {25, 21};

// Vertical lines
Line(24) = {5, 4};
Line(25) = {6, 4};
Line(26) = {7, 5};
Line(27) = {8, 6};

Line(28) = {10, 9};
Line(29) = {11, 9};
Line(30) = {12, 10};
Line(31) = {13, 11};

Line(32) = {14, 1};
Line(33) = {15, 1};
Line(34) = {16, 14};
Line(35) = {17, 15};

Line(36) = {19, 18};
Line(37) = {20, 18};
Line(38) = {21, 19};

Line(39) = {23, 22};
Line(40) = {24, 22};
Line(41) = {25, 23};

//+
nxnear   = 100;
nxfar    = 27;
nxmid    = 50; // wake of prism
nyinlet  = 15;
nyinlet2 = 20;
nymid    = 60; // prism sides
nyfar    = 200;
//+
Transfinite Curve {26, 30, 27, 31} = nxfar Using Progression 1.00;
Transfinite Curve {34, 35} = nxfar Using Progression 1.0;
Transfinite Curve {37, 38} = nxfar Using Progression 1.0;
Transfinite Curve {40, 41} = nxfar Using Progression 1.0;

Transfinite Curve {24, 25} = nxnear Using Progression 0.97;
Transfinite Curve {28, 29} = nxnear Using Progression 0.97;
Transfinite Curve {32, 33} = nxnear Using Progression 0.95;
Transfinite Curve {16, 17} = nxnear Using Progression 0.96;

Transfinite Curve {3} = nxmid Using Bump 0.2;
Transfinite Curve {36} = nxmid Using Bump 0.5;
Transfinite Curve {39} = nxmid Using Bump 0.9;

Transfinite Curve {4} = nyinlet Using Progression 0.996;
Transfinite Curve {5, 6, 7, 8} = nyinlet Using Progression 1;
Transfinite Curve {9} = nyinlet2 Using Progression 0.97;
Transfinite Curve {10, 11} = nyinlet2 Using Progression 1;
Transfinite Curve {12, 13} = nyinlet2 Using Bump 1.8;
Transfinite Curve {1, 2} = nymid Using Bump 0.24;
Transfinite Curve {14, 15} = nymid Using Bump 0.3;
Transfinite Curve {18, 19} = nymid Using Bump 0.4;
Transfinite Curve {20, 21, 22, 23} = nyfar Using Progression 0.99;
//+
Curve Loop(1) = {24, 4, -28, -5};
Plane Surface(1) = {1};
Curve Loop(2) = {25, 4, -29, -6};
Plane Surface(2) = {2};
Curve Loop(3) = {26, 5, -30, -7};
Plane Surface(3) = {3};
Curve Loop(4) = {27, 6, -31, -8};
Plane Surface(4) = {4};
Curve Loop(5) = {28, 9, -32, -10};
Plane Surface(5) = {5};
Curve Loop(6) = {29, 9, -33, -11};
Plane Surface(6) = {6};
Curve Loop(7) = {30, 10, -34, -12};
Plane Surface(7) = {7};
Curve Loop(8) = {31, 11, -35, -13};
Plane Surface(8) = {8};
Curve Loop(9) = {32, 1, -16, 14};
Plane Surface(9) = {9};
Curve Loop(10) = {33, 2, -17, 15};
Plane Surface(10) = {10};
Curve Loop(11) = {3, -16, -36, 17};
Plane Surface(11) = {11};
Curve Loop(12) = {34, -14, -37, -18};
Plane Surface(12) = {12};
Curve Loop(13) = {35, -15, -38, -19};
Plane Surface(13) = {13};
Curve Loop(14) = {36, -20, -39, 21};
Plane Surface(14) = {14};
Curve Loop(15) = {37, -20, -40, 22};
Plane Surface(15) = {15};
Curve Loop(16) = {38, -21, -41, 23};
Plane Surface(16) = {16};
//+
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
Transfinite Surface {13};
Transfinite Surface {14};
Transfinite Surface {15};
Transfinite Surface {16};
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
Extrude {0, 0, -0.05} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Surface{13}; Surface{14}; Surface{15}; Surface{16}; Layers{20}; Recombine;
}
//+
Physical Surface("Inlet") = {94, 50, 72, 116};
//+
Physical Surface("Outlet") = {366, 344, 388};
//+
Physical Surface("Prism") = {252, 230, 270};
//+
Physical Surface("topWall") = {106, 304, 370, 194};
//+
Physical Surface("botWall") = {128, 216, 326, 392};
//+
Physical Surface("Side") = {3, 1, 2, 4, 7, 5, 6, 8, 13, 10, 9, 12, 15, 14, 16, 11, 349, 107, 63, 85, 129, 217, 173, 151, 195, 305, 239, 261, 327, 371, 393, 283};
//+
Physical Volume("Fluid") = {4, 2, 1, 3, 8, 6, 5, 7, 13, 10, 9, 12, 11, 16, 14, 15};
