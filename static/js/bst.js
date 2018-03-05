
//This code is heavily based on code from 
//http://mbostock.github.io/d3/talk/20111018/tree.html 


// Click a node: decrease key
// Need to be able to add nodes
// remove min


d3.bst = function (d3, canvasID) {  

    //defaults 
    var mw = 0, mh = 50;
    var w, h;
    var i = 0;
    var tree;
    var depthStep = 50;
    var canvasID = canvasID; //canvasID must have hash like "#vis" or "#canvas;


    function toggle (d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
    }


    function update(source) {


        var duration = 600;
    
        // Compute the new tree layout.
        var nodes = tree.nodes(rt).reverse();
        
        // console.log(canvasID);
        // console.log(source);
        // console.log(nodes);
        // console.log(rt);
        // console.log("\n\n\n"); 
        //always reference last tree that was made. super frusturating. "rt" points to the last tree's root.
        // each time the d3.bst function is called, it overwrites the last one.


        // Normalize for fixed-depth.
        nodes.forEach(function(d) { d.y = d.depth * depthStep; });
        // Update the nodes…
        var node = vis.selectAll("g.node")
            .data(nodes, function(d) { return d.id || (d.id = ++i); });
    
        // Enter any new nodes at the parent's previous position
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) { 
                return "translate(" + source.x0 + "," + source.y0 + ")"; 
            })
            .on("click", function(d) {  
                console.log("Decreasing key " + d.name); 
                decreaseKey(d);
                    // toggle(d); update(d);
            });
    
        nodeEnter.append("rect")
        nodeEnter.append("text")
            .attr("dy", "-4px")
            .attr("x", "-12px")
            // .attr("text-anchor", "start")
            .text(function(d) { return d.name; })
    
        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) { 
                return "translate(" + d.x + "," + d.y + ")"; 
            })
    
        nodeUpdate.select("rect")
            .attr("width",20)
            .attr("height",7)
            .attr("x", "-10px")
            .style("fill", function(d) { 
                return d._children ? "lightsteelblue" : "#fff"; 
            });
    
        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) { 
                return "translate(" + source.x + "," + source.y + ")"; 
            })
            .remove();
    
        // Update the links…
        var link = vis.selectAll("path.link")
            .data(tree.links(nodes), function(d) { 
                return d.target.id; 
            });
    
        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function(d) {
              var o = {x: source.x0, y: source.y0};
              return diagonal({source: o, target: o});
            })
            .transition()
            .duration(duration)
            .attr("d", diagonal);
    
        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);
    
        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function(d) {
              var o = {x: source.x, y: source.y};
              return diagonal({source: o, target: o});
            })
            .remove();
    
        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    //boilerplate stuff
    var bst_obj = {
        make: function (data) {
                var treeheight = data.height;
                h = treeheight * 60
                w = Math.pow(2, treeheight) * 20 + 50

                tree = d3.layout.tree().size([w, h]);
                diagonal = d3.svg.diagonal() 
                    .projection(function(d) { return [d.x, d.y]; });

                /* aggregate width/height into one svg here? Just lay the roots side by side? */
                vis = d3.select(canvasID).append("svg")
                    .attr("width", w)
                    .attr("height", h)
                    .append("g")
                    .attr("transform", "translate(" + mw + "," + mh + ")");
                rt = data;
                rt.x0 = (w) / 2;
                rt.y0 = 0;
                
                update(rt);
            }
        };
    return bst_obj;
    
};
