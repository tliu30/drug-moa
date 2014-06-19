var width = 960,
    height = 500;

var n = 100,
    nodes = d3.range(n).map(function() { return {}; }),
    links = d3.range(n).map(function(d) { return {source: d, target: (d + 3) % n}; });

var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .size([width, height]);

var svg = d3.select("svg");

var loading = svg.append("text")
    .attr("x", width / 2)
    .attr("y", height / 2)
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text("Simulating. One moment please…");

// Use a timeout to allow the rest of the page to load first.
setTimeout(function() {

  // Run the layout a fixed number of times.
  // The ideal number of times scales with graph complexity.
  // Of course, don't run too long—you'll hang the page!
  force.start();
  for (var i = n * n; i > 0; --i) force.tick();
  force.stop();

  svg.selectAll("line")
      .data(links)
    .enter().append("line")
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  svg.selectAll("circle")
      .data(nodes)
    .enter().append("circle")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("r", 4.5);

  loading.remove();
}, 10);
