/* graph.js
   -----------------------------------
   Functions for loading the network
   visualizations using d3js. */

/* Set size of SVG based on curr window size */
var svg = d3.select("#graph")
    .attr("width", "100%")
    .attr("height", "100%);

/* Appropriately update size of nav bar */
d3.select("#nav").style("height", svg.style("height"));

/* Get force layout initialized */
var force = d3.layout.force()
    .charge(-120)
    .linkDistance(200)
    .size([parseInt(svg.style("width")),
           parseInt(svg.style("height"))]);

/* Function for loading graph using traditional spring layout */
function loadGraph() {
    /* Clear prev graph */
    d3.selectAll(".link").remove();
    d3.selectAll(".node").remove();

    /* Grab desired JSON file path and load */
    var clust = document.getElementById("clust");
    var select_clust = clust.selectedOptions[0].value;
    d3.json(select_clust, function(graph) {
        force.nodes(graph.nodes)
             .links(graph.links)
             .start();

        /* Add links */
        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke-width", 1)
            .attr("stroke", "#AAA");

        /* Add nodes */
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)
            .style("fill", "#00F")
            .call(force.drag);

        /* Add labels */
        node.append("title").text(function(d) {return d.name;});

        /* Start graph */
        force.on("tick", function() {
            link.attr("x1", function(d) {return d.source.x;})
                .attr("y1", function(d) {return d.source.y;})
                .attr("x2", function(d) {return d.target.x;})
                .attr("y2", function(d) {return d.target.y;});

            node.attr("cx", function(d) {return d.x;})
                .attr("cy", function(d) {return d.y;});
        });
    });
};

/* Function for loading graph with radial layout */
        
