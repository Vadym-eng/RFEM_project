from RFEM.initModel import Model, CalculateSelectedCases
from RFEM.LoadCasesAndCombinations.loadCase import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.Results.resultTables import *
from RFEM.BasicObjects.node import Node
from RFEM.TypesForSurfaces.surfaceStiffnessModification import *
from RFEM.BasicObjects.surface import *
from RFEM.BasicObjects.line import *
from RFEM.BasicObjects.thickness import *
from RFEM.Results.resultTables import *
from RFEM.Loads.surfaceLoad import SurfaceLoad
from decimal import Decimal as D
import math as mt
import pandas as pd
import numpy as np


Model(new_model=False, model_name="Surface_2_unification", delete=True)
Model.clientModel.service.begin_modification()
LoadCase(1, "LC 1", [False], ActionCategoryType.ACTION_CATEGORY_PERMANENT_G)
StaticAnalysisSettings(1, "LC 1", StaticAnalysisType.GEOMETRICALLY_LINEAR)

x = D(1.5)  # длина поверхности (m)
y = D(1.5)  # ширина поверхности
len_wid_surfase = D(0.05)  # размер элемента сетки
Ry = 0.015  # kN/mm^2


def equivalent_stress_in_surface(moment_mx, moment_my, moment_mxy, h):  # kN/cm^2
    return round(
        (
            (6 / h**2)
            * (moment_mx**2 + moment_my**2 - moment_mx * moment_my + 3 * moment_mxy**2)
            ** 0.5
        )
        * 100,
        2,
    )


def required_thickness(moment_mx, moment_my, moment_mxy, Ry):  # mm
    return (
        0.1
        if mt.ceil(
            (
                (
                    (6 / Ry)
                    * (
                        moment_mx**2
                        + moment_my**2
                        - moment_mx * moment_my
                        + 3 * moment_mxy**2
                    )
                    ** 0.5
                )
                ** 0.5
            )
            * 10
        )
        / 10
        == 0
        else mt.ceil(
            (
                (
                    (6 / Ry)
                    * (
                        moment_mx**2
                        + moment_my**2
                        - moment_mx * moment_my
                        + 3 * moment_mxy**2
                    )
                    ** 0.5
                )
                ** 0.5
            )
            * 10
        )
        / 10
    )



def hight_selection(stress, surf_num, surf_old_thikness):
    global x, y, len_wid_surfase, Ry
    if ((x + len_wid_surfase) // len_wid_surfase) * 2 < surf_num <= (
        (x + len_wid_surfase) // len_wid_surfase
    ) * ((y + len_wid_surfase) // len_wid_surfase) - (
        (x + len_wid_surfase) // len_wid_surfase
    ) * 2 or surf_num % (
        (x + len_wid_surfase) // len_wid_surfase
    ) not in [
        1,
        2,
        0,
        ((x + len_wid_surfase) // len_wid_surfase) - 1,
    ]: # проверка на не входимость в зону поверхностей ребер
        non_unificat_thickness = round((stress/Ry) * surf_old_thikness, 1) if round((stress/Ry) * surf_old_thikness, 1) >= 20.0 else 20.0
        return min(math.ceil(non_unificat_thickness / 20) * 20, 200)
    else:
        return 200


def creating_surface_geometry():
    global x, y, len_wid_surfase
    count_nodes = 1
    count_lines = 1


    # цикл создания точек
    for i in np.arange(0, x + len_wid_surfase, len_wid_surfase):
        for j in np.arange(0, y + len_wid_surfase, len_wid_surfase):
            Node(
                count_nodes,
                i,
                j,
                0,
            )
            count_nodes += 1

    # цикл создания линий по y
    for i in range(
        1,
        int(
            (x + len_wid_surfase)
            / len_wid_surfase
            * (y + len_wid_surfase)
            / len_wid_surfase
        )
        + 1,
    ):
        if (
            int(i // (x / len_wid_surfase)) != int(i % (x / len_wid_surfase))
            and i % round((x / (len_wid_surfase**2)) * x + x / len_wid_surfase) != 0
        ):
            Line(count_lines, f"{i} {i+1}")
            count_lines += 1

    # цикл создания линий по x
    for j in range(int((x + len_wid_surfase) / len_wid_surfase) + 1):
        for i in range(
            1,
            int(
                (x + len_wid_surfase)
                / len_wid_surfase
                * (y + len_wid_surfase)
                / len_wid_surfase
            )
            + 1,
            int((x + len_wid_surfase) // len_wid_surfase) + 1,
        ):
            if i + (x + len_wid_surfase) // len_wid_surfase + 1 + j <= (
                (x + len_wid_surfase) // len_wid_surfase + 1
            ) * ((x + len_wid_surfase) // len_wid_surfase + 1):

                Line(
                    count_lines,
                    f"{i+j} {i+(x + len_wid_surfase) // len_wid_surfase + 1 + j}",
                )
                count_lines += 1

    # цикл создания поверхностей
    for j in range(0, int((x + len_wid_surfase) / len_wid_surfase)):

        for i in range(1, int((x + len_wid_surfase) / len_wid_surfase) + 1):

            Thickness(
                no=i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
                name="Uniform | d : 200.0 mm | 2 - P235GH 1.0345",
                material_no=3,
                uniform_thickness_d=0.2,
            )

            Surface.WithoutMemberaneTension(
                i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
                geometry_type=SurfaceGeometry.GEOMETRY_PLANE,
                boundary_lines_no=f"{i + j*(int(((x) + len_wid_surfase) / len_wid_surfase))} {(i-1)*int((x + len_wid_surfase) // len_wid_surfase) + 2 + int((x + len_wid_surfase) // len_wid_surfase * (y + len_wid_surfase) // len_wid_surfase) + j} {(i)*int((x + len_wid_surfase) // len_wid_surfase) + 2 + int((x + len_wid_surfase) // len_wid_surfase * (y + len_wid_surfase) // len_wid_surfase) + j} {i + int((x + len_wid_surfase) // len_wid_surfase) + int((x + len_wid_surfase) // len_wid_surfase) * j}",
                thickness=i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
            )
            # Surface.Standard(
            #     i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
            #     geometry_type=SurfaceGeometry.GEOMETRY_PLANE,
            #     boundary_lines_no=f"{i + j*(int(((x) + len_wid_surfase) / len_wid_surfase))} {(i-1)*int((x + len_wid_surfase) // len_wid_surfase) + 2 + int((x + len_wid_surfase) // len_wid_surfase * (y + len_wid_surfase) // len_wid_surfase) + j} {(i)*int((x + len_wid_surfase) // len_wid_surfase) + 2 + int((x + len_wid_surfase) // len_wid_surfase * (y + len_wid_surfase) // len_wid_surfase) + j} {i + int((x + len_wid_surfase) // len_wid_surfase) + int((x + len_wid_surfase) // len_wid_surfase) * j}",
            #     thickness=i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
            # )

    # цикл создания нагрузок на поверхности
    for j in range(0, int((x + len_wid_surfase) / len_wid_surfase)):

        for i in range(1, int((x + len_wid_surfase) / len_wid_surfase) + 1):
            # count_loads.append(str(i + j * (int(((x) + len_wid_surfase) / len_wid_surfase))))
            SurfaceLoad(
                no=i + j * (int(((x) + len_wid_surfase) / len_wid_surfase)),
                load_case_no=1,
                surface_no=f"{i + j * (int(((x) + len_wid_surfase) / len_wid_surfase))}",
                magnitude=50000.0,  # нагрузка 0.5 kg/cm^2 в n/m^2
            )
            # SurfaceLoad(no=1, load_case_no=1, surface_no=f"{" ".join(count_loads)}", magnitude=5000.0)


try:
    Surface.GetSurface(1)
except Exception:
    creating_surface_geometry()


def subsurface_calculation():

    global x, y, len_wid_surfase, Ry

    CalculateSelectedCases([1])

    forces, thickness_new, stress, thickness_old, conv_percent = [[] for _ in range(5)]

    for i in range(1, round(x / len_wid_surfase * y / len_wid_surfase) + 1):
        surface_forces = ResultTables.SurfacesBasicInternalForces(
            loading_type=CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
            loading_no=1,
            object_no=i,
        )
        moment_mx, moment_my, moment_mxy = (
            abs(round(surface_forces[0]["moment_mx"] / 1000, 2)),
            abs(round(surface_forces[0]["moment_my"] / 1000, 2)),
            abs(round(surface_forces[0]["moment_mxy"] / 1000, 2)),
        )  # kNm/m или kNmm/mm

        if not mt.isnan(moment_mx):

            equivalent_stresses = ResultTables.SurfacesEquivalentStressesMises(
                loading_type=CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
                loading_no=1,
                object_no=i,
            )
            equivalent_stress_max = round(
                equivalent_stresses[0]["equivalent_stresses_sigma_eqv_max"]
                / 1000000000,
                3,
            )  # kN/mm^2

            surface_thickness_old = Surface.GetSurface(i).thickness  # mm
            surface_thickness_old_res = (
                Thickness.GetThickness(
                    object_index=surface_thickness_old
                ).uniform_thickness
                * 1000
            )
            thickness_old.append(surface_thickness_old_res)

            forces.append(
                (moment_mx, moment_my, moment_mxy)
            )  # заполнение списка значениями усилий (Mx, My, Mxy) на поверхности (kNm/m или kNmm/mm)

            stress.append(
                round(equivalent_stress_max * 100, 1)
            )  #  заполнение списка экв. напряжениями (σ) (kN/cm^2)

            surface_thickness_new = hight_selection(equivalent_stress_max, i, surface_thickness_old)  # mm

            thickness_new.append(
                surface_thickness_new
            )  # заполнение списка новой толщиной (h) (mm)

            conv_percent.append(
                round(abs(1 - (thickness_new[i - 1] / thickness_old[i - 1])), 2)
            )  # заполнение списка процентом схождения старой и новой толщины %

        else:
            surface_thickness_old = Surface.GetSurface(i).thickness
            surface_thickness_old_res = (
                Thickness.GetThickness(
                    object_index=surface_thickness_old
                ).uniform_thickness
                * 1000
            )
            thickness_old.append(surface_thickness_old_res), forces.append(
                (moment_mx, moment_my, moment_mxy)
            ), stress.append(Ry * 100), thickness_new.append(20.0), conv_percent.append(
                round(abs(1 - (thickness_new[i - 1] / thickness_old[i - 1])), 2)
            )

    for i in range(1, round(x / len_wid_surfase * y / len_wid_surfase) + 1):

        Thickness(
            no=i,
            name=f"Uniform | d : {thickness_new[i - 1]} mm | 2 - P235GH 1.0345",
            material_no=3,
            uniform_thickness_d=thickness_new[i - 1] / 1000,
        )  # назначение результатов поверхности (h)

    Model.clientModel.service.delete_all_results()

    return forces, stress, thickness_new, conv_percent


all_data = {}
min_valie_checking_economic_cross_section = Ry * 100 - 1
i = 1
stress1, conv_percent1 = [1], [1]
# min_valie_checking_economic_cross_section <= min(stress1) and
while not (
    (max(stress1) <= Ry * 100 and max(conv_percent1) <= 0.05) or i == 26
):  # проверка результатов итеррации и остановка процесса при при достижении одного из условий (1 - по результатам поверхностей, 2 - по достижению макс итераций)
    forces1, stress1, thickness_new1, conv_percent1 = subsurface_calculation()

    print(f"Значения при {i} итерации")
    print(f"Усилия на поверхностях    {forces1}")
    print(f"Напряжения:               {stress1}")
    print(f"Новые толщины:            {thickness_new1}")
    print(f"Процент схождения:        {conv_percent1}")
    print("\n" * 3)

    columns = [
        f"(Mx, My, Mxy) [kNmm/mm] (i={i})",
        f"σ [kH/cm^2] (i={i})",
        f"h [mm] (i={i+1})",
        f"Проц. схожд. [%] A(i={i+1})/A(i={i})",
    ]

    all_data[columns[0]] = forces1
    all_data[columns[1]] = stress1
    all_data[columns[2]] = thickness_new1
    all_data[columns[3]] = conv_percent1
    i += 1

results_columns = pd.DataFrame(
    all_data,
    index=[i for i in range(1, round(x / len_wid_surfase * y / len_wid_surfase) + 1)],
)
results_columns.to_excel("results_surface_5.xlsx")


Model.clientModel.service.finish_modification()
