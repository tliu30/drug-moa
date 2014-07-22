var width = 800;
var height = 600;

var color = d3.scale.category10();

var force = d3.layout.force()
    .charge(-3000)
    .linkDistance(function(d) {return d.weight * 200;} )
    .size([width, height]);

var svg = d3.select("#graph")

d3.json("./js/8_0.json", function(graph) {
    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var links = svg.selectAll("line.link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke-width", 1)
        .attr("stroke", "#aaa");

    var nodes = svg.selectAll("g.node")
        .data(graph.nodes)

    var nodeBoxs = nodes.enter().append("g")
        .attr("class", "node");

    nodeBoxs.append("circle")
        .attr("r", 8)
        .style("fill", function(d) {return color(d.group); });

    nodeBoxs.append("text")
        .attr("dx", 9)
        .style("text-anchor", "start")
        .style("font-size", "14px")
        .style("font-color", "#000")
        .text(function(d) { return d.name; });

    force.on("tick", function() {
        links.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        nodes.attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")"; });

    });
});
