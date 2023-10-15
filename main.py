from flask import Flask
from flask import render_template
from flask import request
from data_reader import DataReader
import folium
import folium.plugins
import osmnx as ox
import networkx as nx

dr = DataReader()
app = Flask(__name__)

def clearMap(m):
    txt = m.get_root().render()
    with open("data/deleteOnMap") as f:
        t = f.readline()
        txt = txt.replace("</script>\n</html>", t+"</script>\n</html>")
    return txt

def atmView(point, distance):
    cluster = folium.plugins.MarkerCluster()
    markers = dr.getAtmInfo(userAddress= point, distance= distance)
    for i in range(len(markers)):
        markers[i].add_to(cluster)
    m = folium.Map(location=point, zoom_start=1).add_child(cluster)
    folium.Marker(location=point, icon=folium.Icon(color="red")).add_to(m)
    folium.Circle(location=point, radius=distance*1000, popup="{} meters".format(distance)).add_to(m)
    ret = clearMap(m)
    return ret

def officeView(point, distance):
    cluster = folium.plugins.MarkerCluster()
    markers = dr.getOfficeInfo(userAddress=point, currentTime=[4, 15, 43], distance=distance)
    for i in range(len(markers)):
        markers[i].add_to(cluster)
    m = folium.Map(location=point, zoom_start=1).add_child(cluster)
    folium.Marker(location=point, icon=folium.Icon(color="red")).add_to(m)
    folium.Circle(location=point, radius=distance*1000, popup="{} meters".format(distance)).add_to(m)
    ret = clearMap(m)
    return ret

def shortestWay(start, end, mode = "walk", optimizer="time"):
    ox.config(log_console=True, use_cache=True)
    graph = ox.graph_from_point(start, network_type = mode, simplify=True)
    orig_node = ox.nearest_nodes(graph, start[1], start[0])
    dest_node = ox.nearest_nodes(graph, end[1], end[0])
    shortest_way = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer)
    m = ox.plot_route_folium(graph, shortest_way)
    folium.Marker(location=start, icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(location=end, icon=folium.Icon(color="blue")).add_to(m)
    ret = clearMap(m)
    return ret

@app.route("/test", methods=["GET", "POST"])
def test():
    point = [55.994026, 37.213196]
    return officeView(point, 2)
    

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        pass
        return 0
    if request.method == "POST":
        if request.form["check"] == "Составить маршрут":
            st = list(map(float, request.form["coords"].split()))
            print(st)
            return shortestWay(st[0:2], st[2:4])