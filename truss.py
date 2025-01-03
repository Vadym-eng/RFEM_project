from RFEM.initModel import Model, CalculateSelectedCases
from RFEM.LoadCasesAndCombinations.loadCase import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.Results.resultTables import *
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.section import Section
import math as mt
import pandas as pd

Ry = 23.5

Model(new_model=False, model_name="Ферма(маленькая)(python)", delete=True)
Model.clientModel.service.begin_modification()
LoadCase(1, "LC 1", [True, 0, 0, 1])
StaticAnalysisSettings(1, "LC 1", StaticAnalysisType.GEOMETRICALLY_LINEAR)
Model.clientModel.service.delete_all_results()
CalculateSelectedCases([1])


# подсет стержней
def count_elements():
    count = 0
    while True:
        try:
            a = Member.GetMember(count + 1)
            count += 1
        except Exception:
            break
    return count


num1 = count_elements()


# начало расчета
def truss_member_calculation(num, Ry1):
    forces1, forces_new1, side1, sect1, stress1, old_sect1, conv_percent1 = [
        [] for _ in range(7)
    ]

    # получение старых значений A, N; подбо нового A, % сходимости
    for i in range(1, num + 1):

        member_forces = ResultTables.MembersInternalForces(
            loading_type=CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
            loading_no=1,
            object_no=i,
        )
        forces1.append(
            abs(round(member_forces[0]["internal_force_n"] / 1000, 2))
        )  # заполнение списка значениями усилий N в стержнях (kN)

        memb_member = Member.GetMember(i).section_start
        sekt_memberA = Section.GetSection(memb_member).A

        old_sect1.append(
            round(sekt_memberA * 10000, 3)
        )  # заполнение списка старыми сечениями (A) (cm^2)

        sect1.append(
            0.01
            if round((forces1[i - 1] / Ry1), 3) == 0
            else round((forces1[i - 1] / Ry1), 3)
        )  # заполнение списка новыми сечениями (A) (cm^2)

        conv_percent1.append(
            round(abs(1 - (sect1[i - 1] / old_sect1[i - 1])), 2)
        )  # заполнение списка процентом схождения старого и нового сечения %

        side1.append(
            0.1
            if mt.ceil(mt.sqrt(sect1[i - 1]) * 100) / 10000 == 0
            else mt.ceil(mt.sqrt(sect1[i - 1]) * 100) / 10000
        )  # вычисление стороны квадрата (a) по информации из списка (m)

        Section(
            no=memb_member, name=f"SQ_M1 {side1[i-1]}", material_no=1
        )  # назначение результатов стержня (a)

    Model.clientModel.service.delete_all_results()
    CalculateSelectedCases([1])

    # получение нового значения N и σ
    for i in range(1, num + 1):
        member_forces1 = ResultTables.MembersInternalForces(
            loading_type=CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
            loading_no=1,
            object_no=i,
        )
        forces_new1.append(
            abs(round(member_forces1[0]["internal_force_n"] / 1000, 2))
        )  # заполнение списка новыми значениями усилий (N) в стержнях (kN)

        stress1.append(
            round((forces_new1[i - 1] / sect1[i - 1]), 2)
        )  # заполнение списка напряжениями (σ) (kH/cm^2)
    return (
        sect1,
        [round(i * 100, 2) for i in side1],
        conv_percent1,
        forces_new1,
        stress1,
        forces1,
        old_sect1,
    )


# вывод результатов
all_data = {}
min_valie_checking_economic_cross_section = Ry - 2
i = 9
stress, conv_percent = [1], [1]

while not (
    (
        min_valie_checking_economic_cross_section <= min(stress)
        and max(stress) <= Ry
        and max(conv_percent) <= 0.05
    )
    or i == 40
):  # проверка результатов итеррации и остановка процесса при при достижении одного из условий (1 - по результатам стержней, 2 - по достижению макс итераций)
    i += 1
    sect, side, conv_percent, forces_new, stress, forces, old_sect = (
        truss_member_calculation(num1, Ry)
    )
    print(f"Значения при {i+1} итерации")
    print(f"Усилия в стержнях(стар)   {forces}")
    print(f"Старые сечения:           {old_sect}")
    print(f"Новые сечения:            {sect}")
    print(f"Процент схождения:        {conv_percent}")
    print(f"Сторона квадрата:         {side}")
    print(f"Усилия в стержнях(нов):   {forces_new}")
    print(f"Напряжения:               {stress}")
    print("\n" * 3)

    columns = [
        f"A [см^2] (i={i})",
        f"a [см] (i={i})",
        f"Проц. схожд. [%] A(i={i})/A(i={i-1})",
        f"N [кН] (i={i-1})",
        f"σ [kH/cm^2] (i={i})",
    ]

    all_data[columns[0]] = sect
    all_data[columns[1]] = side
    all_data[columns[2]] = conv_percent
    all_data[columns[3]] = forces_new
    all_data[columns[4]] = stress

results_columns = pd.DataFrame(all_data, index=[i for i in range(1, num1 + 1)])
results_columns.to_excel("results.xlsx")

Model.clientModel.service.finish_modification()
