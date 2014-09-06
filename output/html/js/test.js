var qute = 0;
d3.json('./sources.json', function(thing) {
    probe = document.getElementById("probe");
    for (var x in thing) {
        probe.innerHTML += '<option value=' + '"' + x + '"' + '>' + x + '</option>';
    };
    probe.selectedIndex = -1;
    qute = thing;
});

var color = d3.scale.category10();

var svg = d3.select("#graph")
    .attr("width", "100%")
    .attr("height", "100%");

d3.select("#nav").style("height", svg.style("height"));

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(200)
    .size([parseInt(svg.style("width")),
           parseInt(svg.style("height"))]);

function loadGraph() {    
    var select = document.getElementById("clust");
    var path   = select.options[select.selectedIndex].value;

    d3.selectAll(".link").remove();
    d3.selectAll(".node").remove();

    d3.json(path, function(graph) {
        force
            .nodes(graph.nodes)
            .links(graph.links)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke-width", 1)
            .attr("stroke", "#AAA");
            /*
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
            */

        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)
            .style("fill", function(d) { return color(d.group); })
            .call(force.drag);

        node.append("title")
            .text(function(d) { return d.name; });

        force.on("tick", function() {
              link.attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    });
};

function updateClustList() {
    var probe = document.getElementById("probe");
    var clust = document.getElementById("clust");

    var selected_probe = probe.options[probe.selectedIndex].value;

    clust.innerHTML = "";
    for (var x in qute[[selected_probe]]) {
        x = qute[[selected_probe]][x];
        clust.innerHTML += '<option value=' + '"' + './' + 
            x + '.json"' + '>' + x + '</option>';
    };
    clust.selectedIndex = -1;
};
