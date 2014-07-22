s = d3.select("#clust");
for (i=0; i < something; i++) {
    var path = something[i]
    var name = something[i].split('/')[1].split('.')[0]
    s.append("option").attr("value", path).text(name);    
}
function updateClustList() {
    var select = document.getElementById("probe");
    var probe  = select.options[select.selectedIndex].value;

    var new_list = something[probe];
    var second = d3.select("#clust");
    for (i=0; i < new_list.length; i++) { 
        var path = new_list[i];
        var name = new_list[i].split('/')[1].split('.')[0];
        second.append("option").attr("value", path).text(name);
    };
};
