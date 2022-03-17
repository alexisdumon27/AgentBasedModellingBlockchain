const url_for_orderbook = new URL("http://localhost:5000")
const url_for_transaction_data = new URL("http://localhost:5000/transactions")
const url_for_wealth_distribution_data = new URL("http://localhost:5000/distribution")
const url_for_wealthiest_agents_data = new URL("http://localhost:5000/wealth")

fetch(url_for_orderbook)
    .then(response=>response.json())
    .then(data => orderbookData = data)
    .then((orderbookData) => console.log(orderbookData))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/USDT:USDT/ETH"]["USDT/ETH"], "USDT/ETH", "usdt_eth_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/USDT:USDT/ETH"]["ETH/USDT"], "ETH/USDT", "eth_usdt_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/BTC:BTC/ETH"]["ETH/BTC"], "ETH/BTC", "eth_btc_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/BTC:BTC/ETH"]["BTC/ETH"], "BTC/ETH", "btc_eth_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/BNB:BNB/ETH"]["ETH/BNB"], "ETH/BNB", "eth_bnb_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["ETH/BNB:BNB/ETH"]["BNB/ETH"], "BNB/ETH", "bnb_eth_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BNB/BTC:BTC/BNB"]["BNB/BTC"], "BNB/BTC", "bnb_btc_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BNB/BTC:BTC/BNB"]["BTC/BNB"], "BTC/BNB", "btc_bnb_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BNB/USDT:USDT/BNB"]["BNB/USDT"], "BNB/USDT", "bnb_usdt_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BNB/USDT:USDT/BNB"]["USDT/BNB"], "USDT/BNB", "usdt_bnb_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BTC/USDT:USDT/BTC"]["BTC/USDT"], "BTC/USDT", "btc_usdt_grid"))
    .then((orderbookData) => createAnOrderBookTable(orderbookData["BTC/USDT:USDT/BTC"]["USDT/BTC"], "USDT/BTC", "usdt_btc_grid"))


fetch(url_for_transaction_data)
    .then(response => response.json())
    .then(data => makeTransactionNumbersGraph(data))

fetch(url_for_wealth_distribution_data)
    .then(response => response.json())
    .then(data => makeWealthDistributionPieChart(data))

fetch(url_for_wealthiest_agents_data)
    .then(response => response.json())
    .then(data => makeWealthyAgentsBarChart(data))

function makeWebPage() {

}

function createAnOrderBookTable(data, exchange_symbol, grid_id) {
    console.log("there should be 6")
    var direction_data = data
    let field_name_amount = "amount_" + exchange_symbol
    let field_name_exchange_price = "exchange_price_" + exchange_symbol
    let field_name_limit_price = "limit_price_" + exchange_symbol
    let data_rows = []
    for (let j = 0; j < 100; j++) {
        let row = {}
        if (direction_data[j] == null) { break }
        field_name_amount = "amount_" + exchange_symbol
        field_name_exchange_price = "exchange_price_" + exchange_symbol
        field_name_limit_price = "limit_price_" + exchange_symbol

        row[field_name_amount] = direction_data[j]['amount']
        row[field_name_exchange_price] = direction_data[j]['exchange_price']
        row[field_name_limit_price] = direction_data[j]['limit_price']
        data_rows.push(row)
    }

    var eGridDiv = document.querySelector("#" + grid_id);
    console.log(document)
    var gridOptions = {
        columnDefs: [ { headerName: exchange_symbol, children: [
                        { headerName: "Amount", field: field_name_amount },
                        { headerName: "Exchange Price", field: field_name_exchange_price },
                        { headerName: "Limit Price", field: field_name_limit_price }]
                },]};
    new agGrid.Grid(eGridDiv, gridOptions);
    gridOptions.api.setRowData(data_rows);
    setInterval(function() {
        console.log("poop")
        datas = $.getJSON( url_for_orderbook, {
            format: "json"
        }).done(function( data ) {
            var direction_data = data[getExchangeSymbolKey(exchange_symbol)][exchange_symbol]
            var data_rows = []
            for (let j = 0; j < 100; j++) {
                let row = {}
                if (direction_data[j] == null) { break }
                row[field_name_amount] = direction_data[j]['amount']
                row[field_name_exchange_price] = direction_data[j]['exchange_price']
                row[field_name_limit_price] = direction_data[j]['limit_price']
                data_rows.push(row)
            }
            // data appears to be wrong !!!
            gridOptions.api.setRowData(data_rows);  
        })
    }, 5000)
}

const exchangeSymbolKeys = ["ETH/USDT:USDT/ETH", "ETH/BTC:BTC/ETH", "ETH/BNB:BNB/ETH", "BNB/BTC:BTC/BNB", "BNB/USDT:USDT/BNB", "BTC/USDT:USDT/BTC"]
function getExchangeSymbolKey(exchange) {
    for (let i = 0; i < exchangeSymbolKeys.length; i++) {
        let exchange_0 = exchangeSymbolKeys[i].split(":")[0]
        let exchange_1 = exchangeSymbolKeys[i].split(":")[1]
        if (exchange_0 == exchange || exchange_1 == exchange) {
            return  exchangeSymbolKeys[i]
        }
    }
}

function makeTransactionNumbersGraph(data){
    let name = "num_transactions_"

    const transaction_data = {
        labels: Array.from(Array(data[name+"ETH/USDT:USDT/ETH"].length).keys()), // length of random one as the x labels (may change later)
        datasets: [{
            label: 'ETH and USDT',
            data: data[name + "ETH/USDT:USDT/ETH"],
            borderColor: 'rgb(75, 172, 192)',
            tension: 0.1
        },{
            label: 'ETH and BNB',
            data: data[name + "ETH/BNB:BNB/ETH"],
            borderColor: 'rgb(27, 192, 192)',
            tension: 0.1
        },{
            label: 'ETH and BTC',
            data: data[name + "ETH/BTC:BTC/ETH"],
            borderColor: 'rgb(75, 192, 127)',
            tension: 0.1
        },{
            label: 'BNB and BTC',
            data: data[name + "BNB/BTC:BTC/BNB"],
            borderColor: 'rgb(27, 192, 127)',
            tension: 0.1
        },{
            label: 'BNB and USDT',
            data: data[name + "BNB/USDT:USDT/BNB"],
            fill: false,
            borderColor: 'rgb(175, 27, 27)',
            tension: 0.1
        },{
            label: 'BTC and USDT',
            data: data[name + "BTC/USDT:USDT/BTC"],
            fill: false,
            borderColor: 'rgb(77, 77, 77)',
            tension: 0.1
        },{
            label: 'Total',
            data: data[name + "total"],
            fill: false,
            borderColor: 'rgb(27, 27, 27)',
            tension: 0.1
        }]
    };
    const config = {
        type: 'line',
        data: transaction_data,
        options: {}
    };
    const myChart = new Chart(
        document.getElementById('transactions_line_chart'),
        config
    );

}

function makeWealthDistributionPieChart(data) {
    let name = "wealth_distribution_"
    let row_data = []
    row_data.push(["Random", data[name + 'random']])
    row_data.push(["MACD", data[name + 'macd']])
    row_data.push(["RSI", data[name + 'rsi']])
    row_data.push(["Moving Average", data[name + 'moving_average']])
    row_data.push(["Pivot Point", data[name + 'pivot_point']])

    var data = anychart.data.set(row_data);

    var series_0 = data.mapAs({x: 0, value: 1});

    // create a chart and set the data
    var chart = anychart.pie(series_0);

    // set the container id
    chart.container("distribution_pie_chart");
    chart.title("Wealth Distribution by Strategy pie chart")
    // initiate drawing the chart
    chart.draw();
}

// https://www.anychart.com/
function makeWealthyAgentsBarChart(data) {
    let row_data = []
    var number_of_agents = Object.keys(data).length
    for (let i = 0; i < number_of_agents; i ++ ) {
        let name = "wealthy_" + i
        row_data.push([i + 1, data[name]["amount_in_usd"], data[name]["strategy"], data[name]['num_of_transactions'], data[name]['most_traded_currency_pair']])
    }
    var data = anychart.data.set(row_data);

    var series_0 = data.mapAs({x: 0, value: 1});

    // create a column chart
    var chart = anychart.column(series_0);

    var series = chart.getSeries(0);

    // disable the built-in tooltips
    series.tooltip(false);
    // series_0.tooltip(false);
    
    // set the selection mode to single
    chart.interactivity().selectionMode("single-select");
    
    var tooltip = document.getElementById("tooltip");

    /* show a custom tooltip
    when the mouse is over a column */
    chart.listen("pointMouseOver", function(e) {
        tooltip.style.visibility = "visible"; 
        tooltip.innerHTML = "Amount in USD: "+ data.row(e.pointIndex)[1] + ", Strategy name: " + data.row(e.pointIndex)[2] +
                ", Number of Transactions: "+ data.row(e.pointIndex)[3] + ", Most traded currency pair: "+ data.row(e.pointIndex)[4];
    });

    /* hide the custom tooltip
    when the mouse is out of a column */
    chart.listen("pointMouseOut", function() {
        tooltip.style.visibility = "hidden";
    });

    // set the position of custom tooltips
    chart.listen("mouseMove", function(e) {
        var clientX = e["offsetX"];
        var clientY = e["offsetY"];

        tooltip.style.left = clientX + 20 + "px";
        tooltip.style.top = clientY + 10 + "px";
        tooltip.style.zIndex = 10000;
        tooltip.style.border = "solid black 2px";
    });

    // set the chart title
    chart.title("Current Top 10 Wealthiest Agents");
    // draw
    chart.container("wealth_bar_chart");
    chart.draw();

    setInterval( function () {
        var datas = $.getJSON( url_for_wealthiest_agents_data, {
            format: "json"
        }).done(function( data ) {
            row_data = []
            let new_number_of_agents = Object.keys(data).length
            for (let i = 0; i < new_number_of_agents; i ++ ) {
                let name = "wealthy_" + i
                row_data.push([i + 1, data[name]["amount_in_usd"], data[name]["strategy"], data[name]['num_of_transactions'], data[name]['most_traded_currency_pair']])
            }
            data = anychart.data.set(row_data);
            for (let i = 0; i < new_number_of_agents; i ++ ) {
                series_0.set(
                    i,      // get index of column column
                    "value",    // get parameter to update
                    row_data[i][1],
                );
            }
        }, 5000)
        }) 
    }