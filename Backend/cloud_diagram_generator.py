import spacy
import networkx as nx
import plotly.graph_objects as go

nlp = spacy.load("en_core_web_lg")

class Diagram:
    def __init__(self):
        self.components = []
        self.connections = []
    
    def add_component(self, component):
        self.components.append(component)
        
    def add_connection(self, connection):
        self.connections.append(connection)
        
    def set_position(self, name, x, y):
        for c in self.components:
            if c.name == name:
                c.x = x
                c.y = y
                break
                
class Component:
    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None
        
class Connection:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
def extract_entities(text):
    doc = nlp(text)
    components = []
    connections = []
    for ent in doc.ents:
        if ent.label_ == "COMPONENT":
            components.append(ent.text)
        if ent.label_ == "CONNECTION":
            connections.append(ent.text)
    return components, connections

def generate_diagram(text):
    diagram = Diagram()
    components, connections = extract_entities(text)
    
    for c in components:
        diagram.add_component(Component(c))
        
    for c in connections:
        src, dst = c.split(" connected to ")
        diagram.add_connection(Connection(src, dst))
        
    layout_diagram(diagram)  
    return diagram

def layout_diagram(diagram):
    g = nx.Graph()
    for c in diagram.components:
        g.add_node(c.name)
    for c in diagram.connections:
        g.add_edge(c.src, c.dst)
    pos = nx.spring_layout(g)
    
    for name, point in pos.items():
        x, y = point
        diagram.set_position(name, x, y)
        
def display_diagram(diagram):
    edge_x = []
    edge_y = []
    for c in diagram.connections:
        x0, y0 = get_pos(diagram, c.src)
        x1, y1 = get_pos(diagram, c.dst)
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for c in diagram.components:
        x, y = get_pos(diagram, c.name)
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )),
        text=get_labels(diagram),
        hoverinfo='text')
        
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Automatically Generated Diagram',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    fig.show()
    
def get_pos(diagram, name):
    for c in diagram.components:
        if c.name == name:
            return c.x, c.y
        
def get_labels(diagram):
    labels = []
    for c in diagram.components:
        labels.append(c.name)
    return labels

def read_input():
    return input("Enter architecture description (quit to exit): ")

def main():
    print("""
    Cloud Architecture Diagram Generator  
  
    Describe your cloud architecture using natural language and I will auto-generate a diagram.
    Enter 'quit' to exit. 
    """)
    
    while True:
        text = read_input()
        if text == "quit":  
            break
        
        diagram = generate_diagram(text) 
        display_diagram(diagram)
        
if __name__ == "__main__":
    main()