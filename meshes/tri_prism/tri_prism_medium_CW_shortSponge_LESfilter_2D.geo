xinlet      = -0.1;
xinlet2     = -0.015;
xoutlet     = 0.2;
xoutlet2    = 0.35;
xtriFront   = 0;
xtriRear    = 0.034641;
xtriRear2   = 0.045;
ynearTri    = 0.02;
ynearInlet1 = 0.03;
ynearInlet  = 0.03;
ynearTriTip = 0.035;
ynearOutlet = 0.035;
yfar        = 0.06;
//+
Point(1) = {xtriFront, 0, 0, 1.0};
Point(2) = {xtriRear, ynearTri, 0, 1.0};
Point(3) = {xtriRear, -ynearTri, 0, 1.0};

//Point(4) = {xinlet, 0, 0, 1.0};
//Point(5) = {xinlet, ynearInlet, 0, 1.0};
//Point(6) = {xinlet, -ynearInlet, 0, 1.0};
//Point(7) = {xinlet, yfar, 0, 1.0};
//Point(8) = {xinlet, -yfar, 0, 1.0};

Point(9)  = {xinlet2, 0, 0, 1.0};
Point(10) = {xinlet2, ynearInlet1, 0, 1.0};
Point(11) = {xinlet2, -ynearInlet1, 0, 1.0};
Point(12) = {xinlet2, yfar, 0, 1.0};
Point(13) = {xinlet2, -yfar, 0, 1.0};

Point(14) = {xtriFront, ynearInlet, 0, 1.0};
Point(15) = {xtriFront, -ynearInlet, 0, 1.0};
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

//Point(26) = {xoutlet2, ynearOutlet, 0, 1.0};
//Point(27) = {xoutlet2, -ynearOutlet, 0, 1.0};
//Point(28) = {xoutlet2, yfar, 0, 1.0};
//Point(29) = {xoutlet2, -yfar, 0, 1.0};
//+
// Lines go outside-inwards or bottom-up or left-right
////// Horizontal lines
Line(1) = {1, 2};
Line(2) = {1, 3};
Line(3) = {3, 2};

//Line(4) = {4, 9};
//Line(5) = {5, 10};
//Line(6) = {6, 11};
//Line(7) = {7, 12};
//Line(8) = {8, 13};

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

//Line(24) = {26, 22};
//Line(25) = {27, 23};
//Line(26) = {28, 24};
//Line(27) = {29, 25};

///// Vertical lines
//Line(28) = {5, 4};
//Line(29) = {6, 4};
//Line(30) = {7, 5};
//Line(31) = {8, 6};

Line(32) = {10, 9};
Line(33) = {11, 9};
Line(34) = {12, 10};
Line(35) = {13, 11};

Line(36) = {14, 1};
Line(37) = {15, 1};
Line(38) = {16, 14};
Line(39) = {17, 15};

Line(40) = {19, 18};
Line(41) = {20, 18};
Line(42) = {21, 19};

Line(43) = {23, 22};
Line(44) = {24, 22};
Line(45) = {25, 23};

//Line(46) = {27, 26};
//Line(47) = {28, 26};
//Line(48) = {29, 27};

//+
nxnear   = 45;
nxfar    = 10;
nxmid    = 50; // wake of prism
nyinlet  = 50;
nyinlet2 = 20;
nymid    = 40; // prism sides
nyfar    = 80;
nyfar2   = 10;
//+
//Transfinite Curve {30, 31} = nxfar Using Progression 0.85;
Transfinite Curve {34, 35} = nxfar Using Progression 0.91;
Transfinite Curve {38, 39} = nxfar Using Progression 1;
Transfinite Curve {41, 42} = nxfar Using Progression 0.91;
Transfinite Curve {44, 45} = nxfar Using Progression 0.8;
//Transfinite Curve {47, 48} = nxfar Using Progression 0.8;

//Transfinite Curve {28, 29} = nxnear Using Progression 0.98;
Transfinite Curve {32, 33} = nxnear Using Progression 0.95;
Transfinite Curve {36, 37} = nxnear Using Progression 0.85;
Transfinite Curve {16, 17} = nxnear Using Progression 0.88;

Transfinite Curve {3} = nxmid Using Bump 0.03;
Transfinite Curve {40} = nxmid Using Bump 1.4;
Transfinite Curve {43} = nxmid Using Bump 0.6;
//Transfinite Curve {46} = nxmid Using Bump 0.7;

//Transfinite Curve {4} = nyinlet Using Progression 1;
//Transfinite Curve {5, 6} = nyinlet Using Progression 0.996;
//Transfinite Curve {7, 8} = nyinlet Using Progression 0.992;
Transfinite Curve {9} = nyinlet2 Using Progression 0.9;
Transfinite Curve {10, 11, 12, 13} = nyinlet2 Using Progression 0.99;
Transfinite Curve {1, 2} = nymid Using Bump 0.02;
Transfinite Curve {14, 15} = nymid Using Progression 0.99;
Transfinite Curve {18, 19} = nymid Using Progression 1.015;
Transfinite Curve {20, 21, 22, 23} = nyfar Using Progression 0.99;
//Transfinite Curve {24, 25, 26, 27} = nyfar2 Using Progression 0.69;
//+
//
//Curve Loop(1) = {28, 4, -32, -5};
//Plane Surface(1) = {1};
//Curve Loop(2) = {29, 4, -33, -6};
//Plane Surface(2) = {2};
//Curve Loop(3) = {30, 5, -34, -7};
//Plane Surface(3) = {3};
//Curve Loop(4) = {31, 6, -35, -8};
//Plane Surface(4) = {4};
Curve Loop(5) = {32, 9, -36, -10};
Plane Surface(5) = {5};
Curve Loop(6) = {33, 9, -37, -11};
Plane Surface(6) = {6};
Curve Loop(7) = {34, 10, -38, -12};
Plane Surface(7) = {7};
Curve Loop(8) = {35, 11, -39, -13};
Plane Surface(8) = {8};
Curve Loop(9) = {36, 1, -16, 14};
Plane Surface(9) = {9};
Curve Loop(10) = {37, 2, -17, 15};
Plane Surface(10) = {10};
Curve Loop(11) = {3, -16, -40, 17};
Plane Surface(11) = {11};
Curve Loop(12) = {38, -14, -41, -18};
Plane Surface(12) = {12};
Curve Loop(13) = {39, -15, -42, -19};
Plane Surface(13) = {13};
Curve Loop(14) = {40, -20, -43, 21};
Plane Surface(14) = {14};
Curve Loop(15) = {41, -20, -44, 22};
Plane Surface(15) = {15};
Curve Loop(16) = {42, -21, -45, 23};
Plane Surface(16) = {16};
//Curve Loop(17) = {43, -24, -46, 25};
//Plane Surface(17) = {17};
//Curve Loop(18) = {44, -24, -47, 26};
//Plane Surface(18) = {18};
//Curve Loop(19) = {45, -25, -48, 27};
//Plane Surface(19) = {19};
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
Transfinite Surface {17};
Transfinite Surface {18};
Transfinite Surface {19};
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
Extrude {0, 0, -0.01} {
  Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Surface{13}; Surface{14}; Surface{15}; Surface{16}; Layers{1}; Recombine;
}
//+
Physical Surface("Inlet", 310) = {98, 54, 76, 120};
//+
Physical Surface("Outlet", 311) = {282, 260, 304};
//+
Physical Surface("Prism", 312) = {168, 146, 186};
//+
Physical Surface("topWall", 313) = {110, 220, 286};
//+
Physical Surface("botWall", 314) = {308, 242, 132};
//+
Physical Surface("Side", 315) = {309, 16, 265, 14, 287, 15, 13, 243, 8, 133, 10, 177, 11, 199, 9, 155, 6, 89, 5, 67, 7, 111, 221, 12};
//+
Physical Volume("Fluid", 316) = {3, 1, 2, 4, 9, 6, 7, 5, 8, 11, 10, 12};
