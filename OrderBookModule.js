var OrderBookModule = function(exchange_symbol, height, width) {

    console.log(exchange_symbol)
    console.log(height)
    console.log(width)

    // var canvas_tag = "<canvas width = '" + width + "' height='" + height + "'";
    // canvas_tag += " style= 'border: 1px dotted'></canvas>";

    // var canvas = $(canvas_tag)[0];
    // $("#elements").append(canvas);

    // var context = canvas.getContext("2d");

    // let divider = document.createElement('div')
    // divider.setAttribute("id","div_" + exchange_symbol);

    // let table_0 = document.createElement('table')
    // let thead_0 = document.createElement('thead')
    // let tbody_0 = document.createElement('tbody')

    // table_0.appendChild(thead_0)
    // table_0.appendChild(tbody_0)

    // let table_1 = document.createElement('table')
    // let thead_1 = document.createElement('thead')
    // let tbody_1 = document.createElement('tbody')

    // table_1.appendChild(thead_1)
    // table_1.appendChild(tbody_1)
    // divider.appendChild(table_1)

    // document.getElementById('body').appendChild(table)

    // // make table_0 header
    // let table_0_row_1 = document.createElement('tr');
    // let table_0_heading_1 = document.createElement('th');
    // table_0_heading_1.innerHTML = "Amount";
    // let table_0_heading_2 = document.createElement('th');
    // table_0_heading_2.innerHTML = "Exchange Price";
    // let table_0_heading_3 = document.createElement('th');
    // table_0_heading_3.innerHTML = "Limit Price";

    // table_0_row_1.appendChild(table_0_heading_1);
    // table_0_row_1.appendChild(table_0_heading_2);
    // table_0_row_1.appendChild(table_0_heading_3);
    // thead_0.appendChild(table_0_row_1);
    
    // // make table_1 header
    // let table_1_row_1 = document.createElement('tr');
    // let table_1_heading_1 = document.createElement('th');
    // table_1_heading_1.innerHTML = "Amount";
    // let table_1_heading_2 = document.createElement('th');
    // table_1_heading_2.innerHTML = "Exchange Price";
    // let table_1_heading_3 = document.createElement('th');
    // table_1_heading_3.innerHTML = "Limit Price";

    // table_1_row_1.appendChild(table_1_heading_1);
    // table_1_row_1.appendChild(table_1_heading_2);
    // table_1_row_1.appendChild(table_1_heading_3);
    // thead_1.appendChild(table_1_row_1);

      
    this.render = function(data) {
        // DATA is exchange direction specific so ETH/USDT for example
        // do first direction then do second direction
        console.log(data)
        // for (let i = 0; i < 2; i++) {
        //     data_direction = data.items()[i]
        //     for (let j = 0; j < 100; j++) {
        //         if (data_direction[j] == null) { break }
        //         field_name_amount = "amount_" + exchange_symbol
        //         field_name_exchange_price = "exchange_price_" + exchange_symbol
        //         field_name_limit_price = "limit_price_" + exchange_symbol
        //         let row = document.createElement('tr')
        //         let row_data_1 = document.createElement('td')
        //         row_data_1.innerHTML = data_direction[j]['amount']
        //         let row_data_2 = document.createElement('td')
        //         row_data_2.innerHTML = data_direction[j]['exchange_price']
        //         let row_data_3 = document.createElement('td')
        //         row_data_3.innerHTML = data_direction[j]['limit_price']

        //         row.appendChild(row_data_1)
        //         row.appendChild(row_data_2)
        //         row.appendChild(row_data_3)

        //         if (i == 0) {
        //             tbody_0.appendChild(row)
        //         } else {
        //             tbody_1.appendChild(row)
        //         }
        //     }
        // }

    }

    this.reset = function() {
        // const divider = document.getElementById("div_" + exchange_symbol);
        // while (divider.firstChild) {
        //     divider.removeChild(divider.firstChild);
        // }
    }

}