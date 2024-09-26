# language: en

Feature: Read stock from warehouses

Scenario: Read stock for 1 warehouse
    Given a stock from warehouse amsterdam with the following state
        |SKU_ID:string|Current_Stock_Quantity:int|Units:string|Average_Lead_Time_days:int|Maximum_Lead_Time_days:int|Unit_Price:double|Date:date|Warehouse:string|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|amsterdam|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|amsterdam|
        |1083AA|48210|L|45|68|29,02|2024-09-05|amsterdam|
    When the stock is being processed
    And I retrieve the current state
    Then I expect a stock of 50000 in warehouse amsterdam

Scenario: Read stock for multiple warehouses
    Given a stock from warehouse amsterdam with the following state
        |SKU_ID:string|Current_Stock_Quantity:int|Units:string|Average_Lead_Time_days:int|Maximum_Lead_Time_days:int|Unit_Price:double|Date:date|Warehouse:string|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|amsterdam|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|amsterdam|
        |1083AA|48210|L|45|68|29,02|2024-09-05|amsterdam|
        |1009AA|50000|L|30|48|28,76326|2024-09-07|breda|
        |1077CA|46516|L|45|70|22,9777|2024-09-06|breda|
        |1083AA|48210|L|45|68|29,02|2024-09-05|breda|
    When the stock is being processed
    And I retrieve the current state
    Then I expect a stock of 100000 in warehouse amsterdam

Scenario: A warehouse does not deliver data
    Given nothing is delivered
    When the stock is being processed
    Then I expect an error

    