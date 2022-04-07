var OrderBookModule = function(exchange_symbol, height, width) {
    
    var elementContainer = document.getElementById("elements")
    var table_container = document.createElement('div')
    table_container.style.backgroundColor = "#202E35"
    table_container.style.marginLeft = '-5px'
    table_container.style.marginRight = '-5px'
    table_container.style.paddingTop = '10px'
    table_container.style.border = "0.5px solid grey"
    table_container.style.display = "flex"
    table_container.style.maxHeight = "227px"
    table_container.style.minHeight = "227px"

    // Create TABLE 0 -------------
    let table_0 = document.createElement('table');
    table_0.style.borderCollapse = "collapse"
    table_0.style.borderSpacing = "0"
    table_0.style.width = "100%"
    table_0.style.maxHeight = "100px"
    // Add Title to table_0
    let currency_pairs = exchange_symbol.split(":")
    var title_0 = document.createElement('caption')
    title_0.style.fontSize = "20px"
    title_0.innerHTML = "ORDERBOOK <div style = 'font-size:15px'>" + currency_pairs[0] + "</div>"
    table_0.appendChild(title_0)
    let thead_0 = document.createElement('thead');
    let tbody_0 = document.createElement('tbody');
    tbody_0.style.display = "block;"
    table_0.id = "table_0_" + exchange_symbol
    tbody_0.id = "tbody_0_" + exchange_symbol 
    

    // Style TABLE 0
    thead_0.style.border = "1px solid"
    // thead_0.style.backgroundColor = '#FF0000'
    tbody_0.style.border = "1px solid"
    tbody_0.style.height = "100%"
    
    // append styled TABLE 0
    table_0.appendChild(thead_0);
    table_0.appendChild(tbody_0);

    let table_0_wrapper = document.createElement('div')
    table_0_wrapper.style.float = "left"
    table_0_wrapper.style.width = "50%"
    table_0_wrapper.style.padding = "5px"
    table_0_wrapper.style.border = "5px"
    table_0_wrapper.style.overflow = "auto"
    table_0_wrapper.appendChild(table_0)
    table_container.appendChild(table_0_wrapper);


    // Create TABLE 1 --------------
    let table_1 = document.createElement('table');
    table_1.style.borderCollapse = "collapse"
    table_1.style.borderSpacing = "0"
    table_1.style.width = "100%"
    table_0.style.maxHeight = "100px"
    var title_1 = document.createElement('caption')
    title_1.style.fontSize = "20px"
    title_1.style.paddingTop = "36px"
    title_1.innerHTML = "<div style = 'font-size:15px'>" + currency_pairs[0] + "</div>"
    table_1.appendChild(title_1)
    let thead_1 = document.createElement('thead');
    // thead_1.style.position = "sticky"
    // thead_1.style.top = "0"
    let tbody_1 = document.createElement('tbody');
    tbody_1.style.display = "block;"
    tbody_1.id = "tbody_1_" + exchange_symbol 

    // Style TABLE 1
    thead_1.style.border = "1px solid"
    tbody_1.style.border = "1px solid"
    tbody_1.style.height = "100%"

    table_1.appendChild(thead_1);
    table_1.appendChild(tbody_1);

    let table_1_wrapper = document.createElement('div')
    table_1_wrapper.style.float = "left"
    table_1_wrapper.style.width = "50%"
    table_1_wrapper.style.padding = "5px"
    table_1_wrapper.style.overflow = "auto"
    table_1_wrapper.appendChild(table_1)

    table_container.appendChild(table_1_wrapper);


    // make table_0 header
    let table_0_row_1 = document.createElement('tr');
    let table_0_heading_1 = document.createElement('th');
    table_0_heading_1.innerHTML = "AMOUNT" ;
    table_0_heading_1.style.color = "#d5d9e0"
    let table_0_heading_2 = document.createElement('th');
    table_0_heading_2.innerHTML = "EXCHANGE PRICE";
    table_0_heading_2.style.color = "#d5d9e0"
    let table_0_heading_3 = document.createElement('th');
    table_0_heading_3.innerHTML = "LIMIT PRICE";
    table_0_heading_3.style.color = "#d5d9e0"

    table_0_row_1.appendChild(table_0_heading_1);
    table_0_row_1.appendChild(table_0_heading_2);
    table_0_row_1.appendChild(table_0_heading_3);
    thead_0.appendChild(table_0_row_1);

    // make table_1 header
    let table_1_row_1 = document.createElement('tr');
    table_1_row_1.style.color = "#f0f2f5"
    let table_1_heading_1 = document.createElement('th');
    table_1_heading_1.innerHTML = "AMOUNT";
    // table_1_heading_1.style.color = "#d5d9e0"
    let table_1_heading_2 = document.createElement('th');
    table_1_heading_2.innerHTML = "EXCHANGE PRICE";
    // table_1_heading_2.style.color = "#d5d9e0"
    let table_1_heading_3 = document.createElement('th');
    table_1_heading_3.innerHTML = "LIMIT PRICE";
    // table_1_heading_3.style.color = "#d5d9e0"

    table_1_row_1.appendChild(table_1_heading_3);
    table_1_row_1.appendChild(table_1_heading_2);
    table_1_row_1.appendChild(table_1_heading_1);
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
        
        var number_of_rows = 0

        // find one with most rows of data
        if (Object.keys(data[exchange_symbols[0]]).length > Object.keys(data[exchange_symbols[1]]).length) {
            number_of_rows = Object.keys(data[exchange_symbols[0]]).length
        } else {
            number_of_rows = Object.keys(data[exchange_symbols[1]]).length
        }
        console.log(number_of_rows)
        for (let i = 0; i < 2; i++) {
            data_direction = data[exchange_symbols[i]];
            for (let j = 0; j < number_of_rows; j++) {
                if (data_direction[j] == null) { 
                    break
                }                 
                let row = document.createElement('tr');
                row.style.height = "20px"
                row.style.color = "#f0f2f5"
                let row_data_1 = document.createElement('td');
                let row_data_2 = document.createElement('td');
                let row_data_3 = document.createElement('td');
                row_data_1.innerHTML = parseFloat(data_direction[j]['exchange_price']).toFixed(6);
                row_data_2.innerHTML = parseFloat(data_direction[j]['exchange_price']).toFixed(6);
                row_data_3.innerHTML = parseFloat(data_direction[j]['limit_price']).toFixed(6);
                row.appendChild(row_data_1);
                row.appendChild(row_data_2);
                row.appendChild(row_data_3);
                // edit the style here too as new elements ...

                

                if (i == 0) {
                    tbody_0.appendChild(row);
                } else {
                    tbody_1.appendChild(row);
                }
            }
        }
    };

    this.reset = function () {
        // const divider = document.getElementById("div_" + exchange_symbol);
        while (table_container.firstChild) {
            table_container.removeChild(divider.firstChild);
        }
    };

};