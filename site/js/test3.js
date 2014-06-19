var width = 800;
var height = 600;

var n =  10;
var nodes = [];
var links = [];

d3.json("./js/randhgd.json", function(graph) {
    nodes = graph.nodes;
    links = graph.links;


var force = d3.layout.force()
        .nodes(nodes)
        .links(links)
        .charge(-180)
        .linkDistance(function(d) {return d.weight * 180;})
        .size([width, height]);

var svg = d3.select("svg");

var loading = svg.append("text")
    .attr("x", width / 2)
    .attr("y", height / 2)
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text("Simulating. One moment please...");

setTimeout( function() {
    force.start();
    for (var i = n * n; i > 0; --i) force.tick();
    force.stop();

    svg.selectAll("line").data(links)
        .enter().append("line")
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

    svg.selectAll("circle").data(nodes)
        .enter().append("circle")
            .attr("cx", function(d) {return d.x;})
            .attr("cy", function(d) {return d.y;})
            .attr("r", 4.5);
    loading.remove();
}, 10);
});
