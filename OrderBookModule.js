var OrderBookModule = function(exchange_symbol, height, width) {
    // https://stackoverflow.com/questions/13903952/can-i-draw-a-table-in-canvas-element
    // get element id
    var elementContainer = document.getElementById("elements")

    var table_container = document.createElement('div')
    table_container.style.width = "800px"

    // Create TABLE 0 -------------
    let table_0 = document.createElement('table', );
    let thead_0 = document.createElement('thead');
    let tbody_0 = document.createElement('tbody');
    table_0.id = "table_0_" + exchange_symbol
    tbody_0.id = "tbody_0_" + exchange_symbol 
    
    // Style TABLE 0
    table_0.style.position = "absolute;"
    table_0.style.border = "1px solid"
    table_0.style.float = "left;"
    table_0.style.width = "50%"
    table_0.style.borderCollapse = "collapse"

    thead_0.style.border = "1px solid"
    thead_0.style.backgroundColor = '#FF0000'
    tbody_0.style.border = "1px solid"
    tbody_0.style.height = "200px"
    tbody_0.style.overflow = "auto"
    tbody_0.style.overflowY = "hidden"
    
    // append styled TABLE 0
    table_0.appendChild(thead_0);
    table_0.appendChild(tbody_0);
    table_container.appendChild(table_0);

    // Create TABLE 1 --------------
    let table_1 = document.createElement('table');
    let thead_1 = document.createElement('thead');
    let tbody_1 = document.createElement('tbody');
    tbody_1.id = "tbody_1_" + exchange_symbol 

    // Style TABLE 1
    table_1.style.border = "1px solid"
    table_1.style.float = "left"
    table_1.style.width = "50%"
    table_1.style.borderCollapse = "collapse"
    
    thead_1.style.border = "1px solid"
    thead_1.style.backgroundColor = '#FFFFFF'

    tbody_1.style.border = "1px solid"
    tbody_1.style.height = "200px"
    tbody_1.style.overflow = "auto"
    tbody_1.style.overflowY = "hidden"

    table_1.appendChild(thead_1);
    table_1.appendChild(tbody_1);
    table_container.appendChild(table_1);

    // make table_0 header
    let table_0_row_1 = document.createElement('tr');
    let table_0_heading_1 = document.createElement('th');
    table_0_heading_1.innerHTML = "Amount 0" ;
    let table_0_heading_2 = document.createElement('th');
    table_0_heading_2.innerHTML = "Exchange Price";
    let table_0_heading_3 = document.createElement('th');
    table_0_heading_3.innerHTML = "Limit Price";

    table_0_row_1.appendChild(table_0_heading_1);
    table_0_row_1.appendChild(table_0_heading_2);
    table_0_row_1.appendChild(table_0_heading_3);
    thead_0.appendChild(table_0_row_1);

    // make table_1 header
    let table_1_row_1 = document.createElement('tr');
    let table_1_heading_1 = document.createElement('th');
    table_1_heading_1.innerHTML = "Amount 1";
    let table_1_heading_2 = document.createElement('th');
    table_1_heading_2.innerHTML = "Exchange Price";
    let table_1_heading_3 = document.createElement('th');
    table_1_heading_3.innerHTML = "Limit Price";

    table_1_row_1.appendChild(table_1_heading_1);
    table_1_row_1.appendChild(table_1_heading_2);
    table_1_row_1.appendChild(table_1_heading_3);
    thead_1.appendChild(table_1_row_1);

    elementContainer.appendChild(table_container)
    this.render = function (data) {
        // DATA is exchange direction specific so ETH/USDT for example
        // do first direction then do second direction
        
        var element_0 = document.getElementById("tbody_0_" + exchange_symbol);
        if (element_0) {
            while (element_0.firstChild) {
                element_0.removeChild(element_0.lastChild);
            }
        }

        var element_1 = document.getElementById("tbody_1_" + exchange_symbol);
        if (element_1) {
            while (element_1.firstChild) {
                element_1.removeChild(element_1.lastChild);
            }
        }

        let exchange_symbols = exchange_symbol.split(":")
        for (let i = 0; i < 2; i++) {
            data_direction = data[exchange_symbols[i]];
            for (let j = 0; j < 100; j++) {
                if (data_direction[j] == null) { break} 
                let row = document.createElement('tr');
                let row_data_1 = document.createElement('td');
                row_data_1.innerHTML = parseFloat(data_direction[j]['exchange_price']).toFixed(6);
                let row_data_2 = document.createElement('td');
                row_data_2.innerHTML = parseFloat(data_direction[j]['exchange_price']).toFixed(6);
                let row_data_3 = document.createElement('td');
                row_data_3.innerHTML = parseFloat(data_direction[j]['limit_price']).toFixed(6);
                
                // edit the style here too as new elements ...

                row.appendChild(row_data_1);
                row.appendChild(row_data_2);
                row.appendChild(row_data_3);

                if (i == 0) {
                    tbody_0.appendChild(row);
                } else {
                    tbody_1.appendChild(row);
                }
            }
        }
    };

    this.reset = function () {
        const divider = document.getElementById("div_" + exchange_symbol);
        while (divider.firstChild) {
            divider.removeChild(divider.firstChild);
        }
    };

};