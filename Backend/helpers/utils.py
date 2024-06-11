def format_equipment_data(equipments_and_loans):
    # Crea una lista de diccionarios, donde cada diccionario representa un equipo
    equipments = []
    for equipment, loan in equipments_and_loans:
        equipment_dict = {
            'id': equipment.id,
            'name': equipment.name,
            'serial_number': equipment.serial_number,
            'available': loan is None,
            'dateEnd': loan.loan_end_date if loan else None,
        }
        equipments.append(equipment_dict)

    return equipments