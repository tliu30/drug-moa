var width = 800;
var height = 600;

var color = d3.scale.category10();

var force = d3.layout.force()
    .charge(-180)
    .linkDistance(function(d) {return d.weight * 200;} )
    .size([width, height]);

var svg = d3.select("#graph");

d3.json("./js/randhgd.json", function(graph) {
    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var links = svg.selectAll("line.link")
        .data(force.links())
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke-width", 1)
        .attr("stroke", "#aaa");

    var nodes = svg.selectAll("circle.node")
        .data(graph.nodes).enter()
        .append("circle")
        .attr("r", 8)
        .style("fill", function(d) {return color(d.group); });

    console.log(nodes);

    force.on("tick", function() {
        links.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        nodes.attr("cx", function(d) {return d.x})
             .attr("cy", function(d) {return d.y});

    });
});
