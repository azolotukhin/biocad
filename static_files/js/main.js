
        $(document).ready(function() {
            var data = [];

            data.push({"start": "3/23/2015 5:27:00", "end": "3/23/2015 1:27:00", "task":"cc12f9d4-26f1-11e5-80c0-00505692e771"});

            data.push({"start": "3/23/2015 1:27:00", "end": "3/23/2015 10:43:00", "task":"cc12f9d4-26f1-11e5-80c0-00505692e771"});

            // data.push({"start": "3/23/2015 10:43:00", "end": "24/24/2015 5:27:00", "task":"cc12f9d4-26f1-11e5-80c0-00505692e771"});


            //for (var i = 0; i < 541; i++) {
            //   data.push({"start": "4/1/2015 9:00:00", "end": "4/1/2015 9:30:00", "task": "Planning"+i, "order_id": 3});
            //   data.push({"start": "4/1/2015 9:35:00", "end": "4/1/2015 10:00:00", "task": "Planning"+i, "order_id": 4},);
            //   data.push({"start": "4/1/2015 20:35:00", "end": "4/1/2015 21:00:00", "task": "Planning"+i, "order_id": 5},);
            //}
            // var data = [
                // {"start": "4/1/2015 9:00:00", "end": "4/1/2015 9:30:00", "task": "Planning"},
                // {"start": "4/1/2015 9:35:00", "end": "4/1/2015 10:00:00", "task": "Planning"},
                // {"start": "4/1/2015 9:30:00", "end": "4/1/2015 10:30:00", "task": "Development"},
                // {"start": "4/1/2015 10:30:00", "end": "4/1/2015 10:45:00", "task": "QE"}
            // ];

            var colorScale = new Plottable.Scales.Color();
            colorScale.range([].concat(... new Array(100).fill(['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#CFECF9', '#7F7F7F', '#BCBD22', '#17BECF'])));

            var xScale = new Plottable.Scales.Time();
            var xAxis = new Plottable.Axes.Time(xScale, "bottom");

            var yScale = new Plottable.Scales.Category();
            var yAxis = new Plottable.Axes.Category(yScale, "left");

            var plot = new Plottable.Plots.Rectangle()
                .x(function (d) {
                    return new Date(d.start);
                }, xScale)
                .x2(function (d) {
                    return new Date(d.end);
                })
                .y(function (d) {
                    return d.task;
                }, yScale)
                .attr("fill", function (d) {
                    return d.task;
                }, colorScale)
                .addDataset(new Plottable.Dataset(data));

            var chart = new Plottable.Components.Table([
                [yAxis, plot],
                [null, xAxis]
            ]);

            chart.renderTo("svg#example");



            var tooltipAnchorSelection = plot.foreground().append("circle").attr({
              r: 3,
              opacity: 0
            });

            var tooltipAnchor = $(tooltipAnchorSelection.node());
            tooltipAnchor.tooltip({
              animation: false,
              container: "body",
              placement: "auto",
              title: "text",
              trigger: "manual"
            });

            // Setup Interaction.Pointer
            var pointer = new Plottable.Interactions.Pointer();
            pointer.onPointerMove(function(p) {
              var closest = plot.entityNearest(p);
              if (closest) {
                tooltipAnchor.attr({
                  cx: closest.position.x,
                  cy: closest.position.y,
                  "data-original-title": "Value: " + closest.datum.y
                });
                tooltipAnchor.tooltip("show");
              }
            });
        });
