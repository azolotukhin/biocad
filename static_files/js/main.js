
        $(document).ready(function() {
            // var data = [];
            //
            // data.push({"start": "3/23/2019 12:00:00",
            //                     "end": "3/23/2019 5:27:00",
            //                     "task":"cc12f9d4-26f1-11e5-80c0-00505692e771",
            //                     "order_id": 59995 ,
            //                     "amount":340 });
            //
            //         data.push({"start": "3/23/2019 5:27:00",
            //                     "end": "3/23/2019 1:27:00",
            //                     "task":"cc12f9d4-26f1-11e5-80c0-00505692e771",
            //                     "order_id": 88577 ,
            //                     "amount":440 });
            //
            //         data.push({"start": "3/23/2019 1:27:00",
            //                     "end": "3/23/2019 10:43:00",
            //                     "task":"cc12f9d4-26f1-11e5-80c0-00505692e771",
            //                     "order_id": 50475 ,
            //                     "amount":510 });
            //
            //         data.push({"start": "3/23/2019 10:43:00",
            //                     "end": "3/23/2019 11:59:00",
            //                     "task":"cc12f9d4-26f1-11e5-80c0-00505692e771",
            //                     "order_id": 21298 ,
            //                     "amount":370 });
            //
            // // data.push({"start": "3/23/2015 10:43:00", "end": "24/24/2015 5:27:00", "task":"cc12f9d4-26f1-11e5-80c0-00505692e771"});
            //
            //
            // //for (var i = 0; i < 541; i++) {
            // //   data.push({"start": "4/1/2015 9:00:00", "end": "4/1/2015 9:30:00", "task": "Planning"+i, "order_id": 3});
            // //   data.push({"start": "4/1/2015 9:35:00", "end": "4/1/2015 10:00:00", "task": "Planning"+i, "order_id": 4},);
            // //   data.push({"start": "4/1/2015 20:35:00", "end": "4/1/2015 21:00:00", "task": "Planning"+i, "order_id": 5},);
            // //}
            // // var data = [
            //     // {"start": "4/1/2015 9:00:00", "end": "4/1/2015 9:30:00", "task": "Planning"},
            //     // {"start": "4/1/2015 9:35:00", "end": "4/1/2015 10:00:00", "task": "Planning"},
            //     // {"start": "4/1/2015 9:30:00", "end": "4/1/2015 10:30:00", "task": "Development"},
            //     // {"start": "4/1/2015 10:30:00", "end": "4/1/2015 10:45:00", "task": "QE"}
            // // ];
            //
            // var colorScale = new Plottable.Scales.Color();
            // colorScale.range([].concat(... new Array(100).fill(['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#CFECF9', '#7F7F7F', '#BCBD22', '#17BECF'])));
            //
            // var xScale = new Plottable.Scales.Time();
            // var xAxis = new Plottable.Axes.Time(xScale, "bottom");
            //
            // var yScale = new Plottable.Scales.Category();
            // var yAxis = new Plottable.Axes.Category(yScale, "left");
            //
            // var plot = new Plottable.Plots.Rectangle()
            //     .x(function (d) {
            //         return new Date(d.start);
            //     }, xScale)
            //     .x2(function (d) {
            //         return new Date(d.end);
            //     })
            //     .y(function (d) {
            //         return d.task;
            //     }, yScale)
            //     .attr("fill", function (d) {
            //         return d.task;
            //     }, colorScale)
            //     .addDataset(new Plottable.Dataset(data));
            //
            // var chart = new Plottable.Components.Table([
            //     [yAxis, plot],
            //     [null, xAxis]
            // ]);
            //
            // chart.renderTo("svg#example");
            $('#datepicker').datepicker({
                format: 'dd.mm.yyyy',
                uiLibrary: 'bootstrap4'
            });

            $( "#search" ).keyup(function() {
                var order_id = $(this).val();
                if (order_id) {
                    $( "#search-form" ).attr("action", "/order/"+order_id)
                } else {
                    $( "#search-form" ).attr("action", "/")
                }

            });

        });
