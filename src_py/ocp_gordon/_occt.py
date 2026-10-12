"""The OCCT binding ocp_gordon runs on: OCP (cadquery-ocp) or nanocct.

The binding is chosen once, at import: nanocct if it is installed, else OCP.
Installing nanocct is a statement: where both are installed, ocp_gordon and the
other libraries of the OCP/nanocct ecosystem (ocpsvg, ocp-tessellate) all use
nanocct, so that a build123d built on nanocct and the libraries it imports
share one binding. Who wants OCP does not install nanocct.

Every module of ocp_gordon imports its OCCT names from here, so the code is the
same for both bindings; the type checker sees the OCP names. The two bindings
differ in the names of the collection classes (OCP's `Array1_gp_Pnt` is
nanocct's `NCollection_Array1[gp_Pnt]`), which are aliased to OCP's names
below, and in one calling convention, wrapped by `eval_bspline_basis`.
"""

import importlib.util
from typing import TYPE_CHECKING


def _binding() -> str:
    for binding in ("nanocct", "OCP"):
        if importlib.util.find_spec(binding) is not None:
            return binding
    raise ImportError("ocp_gordon needs nanocct or OCP (cadquery-ocp)")


BINDING = _binding()

if TYPE_CHECKING or BINDING == "OCP":
    from OCP.BRep import BRep_Tool
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
    from OCP.BSplCLib import BSplCLib
    from OCP.Geom import (
        Geom_BSplineCurve,
        Geom_BSplineSurface,
        Geom_Circle,
        Geom_Curve,
        Geom_Ellipse,
        Geom_TrimmedCurve,
    )
    from OCP.Geom2dAPI import Geom2dAPI_Interpolate, Geom2dAPI_ProjectPointOnCurve
    from OCP.GeomAbs import GeomAbs_C2, GeomAbs_Shape
    from OCP.GeomAPI import (
        GeomAPI_Interpolate,
        GeomAPI_PointsToBSpline,
        GeomAPI_ProjectPointOnCurve,
    )
    from OCP.GeomConvert import (
        GeomConvert,
        GeomConvert_ApproxCurve,
        GeomConvert_CompCurveToBSplineCurve,
    )
    from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Pnt2d, gp_Trsf, gp_Vec
    from OCP.math import math_Matrix
    from OCP.Precision import Precision
    from OCP.TopoDS import TopoDS_Face
    from OCP.collections import (
        Array1_double,
        Array1_gp_Pnt,
        Array1_int,
        Array2_gp_Pnt,
        HArray1_double,
        HArray1_gp_Pnt,
        HArray1_gp_Pnt2d,
        HArray1_int,
    )
else:
    from nanocct.BRep import BRep_Tool
    from nanocct.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
    from nanocct.BSplCLib import BSplCLib
    from nanocct.Geom import (
        Geom_BSplineCurve,
        Geom_BSplineSurface,
        Geom_Circle,
        Geom_Curve,
        Geom_Ellipse,
        Geom_TrimmedCurve,
    )
    from nanocct.Geom2dAPI import Geom2dAPI_Interpolate, Geom2dAPI_ProjectPointOnCurve
    from nanocct.GeomAbs import GeomAbs_C2, GeomAbs_Shape
    from nanocct.GeomAPI import (
        GeomAPI_Interpolate,
        GeomAPI_PointsToBSpline,
        GeomAPI_ProjectPointOnCurve,
    )
    from nanocct.GeomConvert import (
        GeomConvert,
        GeomConvert_ApproxCurve,
        GeomConvert_CompCurveToBSplineCurve,
    )
    from nanocct.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Pnt2d, gp_Trsf, gp_Vec
    from nanocct.math import math_Matrix
    from nanocct.Precision import Precision
    from nanocct.TopoDS import TopoDS_Face
    # the collection templates are generic classes in nanocct
    from nanocct.NCollection import (
        NCollection_Array1,
        NCollection_Array2,
        NCollection_HArray1,
    )

    Array1_double = NCollection_Array1[float]
    Array1_gp_Pnt = NCollection_Array1[gp_Pnt]
    Array1_int = NCollection_Array1[int]
    Array2_gp_Pnt = NCollection_Array2[gp_Pnt]
    HArray1_double = NCollection_HArray1[float]
    HArray1_gp_Pnt = NCollection_HArray1[gp_Pnt]
    HArray1_gp_Pnt2d = NCollection_HArray1[gp_Pnt2d]
    HArray1_int = NCollection_HArray1[int]


def eval_bspline_basis(
    derivative_order: int,
    order: int,
    flat_knots: Array1_double,
    parameter: float,
    bspline_basis: math_Matrix,
) -> None:
    """BSplCLib::EvalBsplineBasis, filling bspline_basis.

    The bindings differ in the int& out-parameter FirstNonZeroBsplineIndex: OCP
    takes it as an argument, nanocct returns it. ocp_gordon does not use it.
    """
    if BINDING == "OCP":
        BSplCLib.EvalBsplineBasis_s(
            derivative_order, order, flat_knots, parameter, 0, bspline_basis
        )
    else:
        BSplCLib.EvalBsplineBasis_s(
            derivative_order, order, flat_knots, parameter, bspline_basis
        )
