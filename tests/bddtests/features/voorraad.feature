# language: nl

Functionaliteit: Inlezen van voorraard uit warehouses

Scenario: Inlezen voorraad voor 1 warehouse
    Gegeven een voorraad uit het warehouse amsterdam met de volgende stand
        |SKU_ID:string|Current_Stock_Quantity:int|Units:string|Average_Lead_Time_days:int|Maximum_Lead_Time_days:int|Unit_Price:double|Date:date|Warehouse:string|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|amsterdam|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|amsterdam|
        |1083AA|48210|L|45|68|29,02|2024-09-05|amsterdam|
    Als de voorraad wordt verwerkt
    En ik haal de huidige voorraad op
    Dan verwacht ik een voorraad van 50000 in het warehouse amsterdam

Scenario: Inlezen voorraad voor meerdere warehouses
    Gegeven een voorraad uit het warehouse amsterdam met de volgende stand
        |SKU_ID:string|Current_Stock_Quantity:int|Units:string|Average_Lead_Time_days:int|Maximum_Lead_Time_days:int|Unit_Price:double|Date:date|Warehouse:string|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|amsterdam|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|amsterdam|
        |1083AA|48210|L|45|68|29,02|2024-09-05|amsterdam|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|breda|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|breda|
        |1083AA|48210|L|45|68|29,02|2024-09-05|breda|
    Als de voorraad wordt verwerkt
    En ik haal de huidige voorraad op
    Dan verwacht ik een voorraad van 100000 in het warehouse amsterdam

Scenario: Een warehouse levert niks aan
    Gegeven er is niks aangeleverd
    Als de voorraad wordt verwerkt
    Dan verwacht ik een fout

    