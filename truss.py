from RFEM.initModel import Model, Calculate_all
from RFEM.LoadCasesAndCombinations.loadCase import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.Results.resultTables import *
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.section import Section
import math as mt

Ry = 23.5

Model(new_model=False, model_name="Ферма(маленькая)(python)")
Model.clientModel.service.begin_modification()
LoadCase(1, "LC 1", [True, 0, 0, 1])
StaticAnalysisSettings(1, "LC 1", StaticAnalysisType.GEOMETRICALLY_LINEAR)


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

    Calculate_all()
    forces1, forces_new, side1, sect1, stress1, old_sect1, conv_percent = [
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
            round((forces1[i - 1] / Ry1), 3)
        )  # заполнение списка новыми сечениями (A) (cm^2)

        conv_percent.append(
            round(abs((1 - (sect1[i - 1] / old_sect1[i - 1])) * 100), 2)
        )  # заполнение списка процентом схождения старого и нового сечения %

        side1.append(
            mt.ceil(mt.sqrt(sect1[i - 1]) * 100) / 10000
        )  # вычисление стороны квадрата (a) по информации из списка (m)

        Section(
            no=memb_member, name=f"SQ_M1 {side1[i-1]}", material_no=1
        )  # назначение результатов стержня (a)

    Calculate_all()

    # получение нового значения N и σ
    for i in range(1, num + 1):
        member_forces1 = ResultTables.MembersInternalForces(
            loading_type=CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
            loading_no=1,
            object_no=i,
        )
        forces_new.append(
            abs(round(member_forces1[0]["internal_force_n"] / 1000, 2))
        )  # заполнение списка новыми значениями усилий (N) в стержнях (kN)

        stress1.append(
            round((forces_new[i - 1] / sect1[i - 1]), 2)
        )  # заполнение списка напряжениями (σ) (kH/cm^2)
    return forces1, old_sect1, sect1, conv_percent, side1, forces_new, stress1


for i in range(3):
    (
        forces_old,
        sections_old,
        sections_new,
        convergence_percentage,
        square_sides,
        forces_new,
        stresses,
    ) = truss_member_calculation(num1, Ry)
    print(f"Значения при {i+1} итерации")
    print(f"Усилия в стержнях(стар)   {forces_old}")
    print(f"Старые сечения:           {sections_old}")
    print(f"Новые сечения:            {sections_new}")
    print(f"Процент схождения:        {[i*1000 for i in convergence_percentage]}")
    print(f"Сторона квадрата:         {square_sides}")
    print(f"Усилия в стержнях(нов):   {forces_new}")
    print(f"Напряжения:               {stresses}")
    print("\n" * 3)


tk = """while not(Ry-4<=min(a)) and not(max(a)<=Ry) and not(max(b)<= 5):
    a, b = truss_member_calculation(num1, Ry) # где a - напряжение и b - процент схождения"""

Model.clientModel.service.finish_modification()
