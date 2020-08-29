const vis = d3.select("#graph")
            .append("svg")
            .attr("width", 1500)
            .attr("height", 1500);

fetch("/graph.json")
    .then((res) => res.json())
    .then((json) => {
        render(json.nodes, json.links)
    });


function render(nodes, links) {
    const link = vis.selectAll(".line")
   .data(links)
   .enter()
   .append("line")
   .attr("x1", function(d) { return d.source.x })
   .attr("y1", function(d) { return d.source.y })
   .attr("x2", function(d) { return d.target.x })
   .attr("y2", function(d) { return d.target.y })
   .style("stroke", "rgb(6,120,155)");

    const node = vis.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter().append("g")

    const circles = node.append("svg:circle")
        .attr("r", "6px")
        .attr("fill", "black")

    const labels = node.append("text")
        .text(d => d.id)
        .attr('x', 12)
        .attr('y', 3);

    var force = d3.layout.force()
        .nodes(nodes)
        .links(links)
        .size([1500, 1500])
        .linkStrength(0.4)
        .friction(0.9)
        .linkDistance(25)
        .charge(-90)
        .gravity(0.07)
        .theta(0.8)
        .alpha(0.3)
        .start();

    for (var i = 0; i < 80; ++i) {
        force.tick();
    }

    force.on("tick", () => {
      link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
    });
}
