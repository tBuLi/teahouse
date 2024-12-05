import anywidget
import traitlets

SOLUTIONS = {
    'spider1': """
# solution 1
point2 = alg.vector(e0=1, e1=-1, e2=-0.5).dual()

def graph_func():
    # We put all these results within the graph function so that everything will be interactive.
    
    # solution 2 / 4
    line2 = point1 & point2
    
    # solution 3 / 4
    point3 = line1 ^ line2
    
    # solution 6
    point4 = line1 >> point1
    
    # solution 7
    line3 = line1 | point4
    
    # solution 8
    line4 = line2.normalized() + line3.normalized()
    
    return [
        "Spider Workshop - BoilerPlate",
        0xff0000, line1, "line",
        0x540099, point1, "point",
        0x990054, point2, "point2",   # solution 1
        0x0000ff, line2, "line2",     # solution 2
        0x8800ff, point3, "point3",   # solution 3
        0x9000A0, point4, "point4",   # solution 6
        0x888800, line3, "line 3",    # solution 7
        0x008888, line4, "line 4",    # solution 8
    ]

alg.graph(
    graph_func,
    grid=True, labels=True,
)
""",
    'spider2': """
def sw(R, items):
    return [R >> item for item in items]

def graph_func():
    L2 = (P1 & P2).normalized()
    
    # Solution 1, 2
    triangle2 = [L1 >> p for p in triangle1]
    triangle3 = sw(L2, triangle2)  # Alternative way to do the same.
    
    # Solution 3
    triangle3 = [(L2*L1) >> p for p in triangle1]
    
    # Solution 5
    L3 = (L1 + L2).normalized()

    # Solution 6
    triangle4 = [(L3*L1) >> p for p in triangle1]

    # Solution 7
    triangle5 = [P2 >> p for p in triangle1]

    # Solution EXTRA
    triangle4 = [(((L2|alg.blades.e012.dual())+L1)*L1) >> p for p in triangle1]
    
    # now return a list of things to render.
    return [
       "Spider Workshop - Elements are Transformations",
       0x009977, L1, "L1",
       0x009977, L2, "L2", P1, P2,
       0x990077, triangle1, "t1",
       0xff0088, triangle2, "t2",
       0xffdd00, triangle3, "t3",
       0x0000ff, L3, "L3",
       0x00ff55, triangle4, "t4",
       0x007bff, triangle5, "t5",
    ]

alg.graph(
    graph_func,
    grid=True, labels=True,
)
""",
    'spider3': '''
def sw(R, items):
    """ Sandwich all items by R. """
    return [R >> item for item in items]

def graph_func():
    t = timeit.default_timer() % (2 * math.pi)  # Grab the current time modulo 2 pi.
    
    # Below you can write the answers to the exercises so they are animated.
    
    # Solution 1
    R = ( -0.5 * t * P1 ).exp()
    
    # Solution 2
    triangle2 = sw(R, triangle1)

    # Solution 3
    L2 = L1 | alg.blades.e0.dual()  # Dot with the origin
    
    # Solution 4
    P2 = L2.normalized() ^ alg.blades.e0
    
    # Solution 5
    T = ( -0.5 * t * P2 ).exp()
    
    # Solution 6
    triangle3 = sw(T, triangle1)
    
    return [
        "Spider Workshop - Exponentials - around and along",
        0x009977, L1, "L1",
        0x009977, P1, "P1", 
        0x990077, triangle1, "t1",
        0x66ffcc, triangle2, L2, P2,
        0x770099, triangle3,
    ]

alg.graph(
    graph_func,
    grid=True, labels=True, animate=True
)
''',
    'spider4': '''
def inverse_kinematics(C, Base, Target) -> None:
    """Our IK function takes a chain, a base and a target, and updates the chain *in place* to a new chain."""
    # Step 1, set the last point in the chain to the target.
    C[3] = Target
    # Step 2, restore all lengths by moving along the line to the next point.
    for i in reversed(range(3)): 
        C[i] = tr(C[i] & C[i+1], 0.5) >> C[i+1]
    # Step 3, restore to the base
    C[0] = Base
    # Step 4, restore all lengths again by moving along the same line, other direction.
    for i in range(1, 3 + 1):
        C[i] = tr(C[i-1] & C[i], -0.5) >> C[i-1]
''',
    'spider5': '''
def inverse_kinematics(C, Base, Target) -> None:
    """Our IK function takes a chain, a base and a target, and updates the chain *in place* to a new chain."""
    C[3] = Target
    for i in reversed(range(3)): 
        C[i] = tr(C[i] & C[i+1], 0.5) >> C[i+1]
    
    # Here we put our constraints
    # Solution 1
    plane = Base & Target & alg.blades.e2.dual()
    
    # Solution 2
    for i in range(1, len(C)):
        C[i] = (C[i] | plane) / plane
    
    # Solution 3
    plane2 = alg.blades.e13 | Base
    
    # Solution 4
    signed_distance = (plane2 & C[1]).e
    if signed_distance < 0:
        C[1] = (C[1] | plane2) / plane2
        
    # Solution 5
    angle = (((C[1] & C[2] | C[2]) ^ plane) | (C[2] & C[3])).e
    if angle < 0:
        C[2] =  (C[1] & C[3]).normalized() >> C[2]
    
    C[0] = Base
    for i in range(1, 3 + 1):
        C[i] = tr(C[i-1] & C[i], -0.5) >> C[i-1]
''',
    'spider6': '''
import itertools

AXIS = alg.blades.e2 | alg.vector(e0=1, e1=1.3, e2=0, e3=0).dual()
time = 0

def graph_func():
    global time, base
    
    # Grab the time
    time += 1/60
    # Resolve the IK
    for leg, target in zip(legs, targets):
        inverse_kinematics(leg.chain, base, target)
    # move the goals forward
    R = (-0.5*0.5*time*AXIS).exp()
    goals = [R >> g for g in INITIAL_GOALS]
    
    # loop over all legs. If our target is too far from our goal, and the legs before
    # and after us are not active, then we become active.
    for i, leg in enumerate(legs):
        if (targets[i] & goals[i]).norm().e > 0.15 and not leg.active and not legs[(i-1)%8].active and not legs[(i+1)%8].active:
            leg.start = time
            leg.active = True
            leg.pos = 1*targets[i]  # multiply by one to do a deepcopy.

    # loop over all legs, if we are active move our target towards its goal.
    for i, leg in enumerate(legs):
        if not leg.active: 
            continue
        current_time = (time - leg.start)*6
        ct = min(1, current_time)
        targets[i] = (1 - ct)*leg.pos + ct*goals[i] + math.sin(ct*math.pi)*0.1*UP  # LERP from position to goal while lifting up following a sine curve. 
        targets[i] = goals[i]
        if current_time >= 1:
            leg.active = False

    # Update our base to be at the average of our targets but still raised above the plane of the targets.
    base = 0.35 * UP + sum(targets).normalized()
    
    # BONUS: render some shadows by intersecting light rays from a source through each point with the floor. 
    light = alg.vector(e0=1, e1=4, e2=1, e3=4).dual()
    floor = alg.vector(e0=1, e2=1)
    
    # now return a list of things to render.
    return [
        "Spider Workshop - Spider!",
        0xCCCCCC,
        (base & light) ^ floor,
        *map(lambda pair: [(p & light) ^ floor for p in pair], itertools.chain(*[itertools.pairwise(leg.chain) for leg in legs])),
        0x000000,
        *itertools.chain(*[itertools.pairwise(leg.chain) for leg in legs]),  # Know the standard library!
        base, "B",
    ]

alg.graph(
    graph_func,
    grid=True, labels=True, lineWidth=4, pointRadius=4, animate=True,
    width='100%'
)
''',
}

class SolutionWidget(anywidget.AnyWidget):
    """ Simple widget to show/hide the solution to the exercise. """
    _esm = """
    function render({ model, el }) {
      let button = document.createElement("button");
      let div = document.createElement("div");
      let link = document.createElement('link');
      link.href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css";
      link.rel = "stylesheet";
      let script = document.createElement('script');
      script.src = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js";
      let script2 = document.createElement('script2');
      script2.src = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js";
      
      button.innerHTML = `Show Solution`;
      button.classList.add("toggle-button");
      
      div.innerHTML = `<pre><code class="language-python">${model.get("solution")}</code></pre>`;
      div.style.display = "none";
      
      button.addEventListener("click", () => {
        model.set("show", !model.get("show"));
        model.save_changes();
      });
      model.on("change:show", () => {
        if (model.get("show")) {
            button.innerHTML = `Hide Solution`;
            div.style.display = "block";

            // Trigger Prism.js to highlight the code
            Prism.highlightAll();
        } else {
            button.innerHTML = `Show Solution`;
            div.style.display = "none";
        }
      });
      el.appendChild(button);
      el.appendChild(div);
      el.appendChild(script1);
    }
    export default { render };
    """
    _css = """
    .toggle-button {
      background-image: linear-gradient(to right, #a1c4fd, #c2e9fb);
      border: 0;
      border-radius: 10px;
      padding: 10px 50px;
      color: white;
    }
    """
    solution = traitlets.Unicode().tag(sync=True)
    show = traitlets.Bool(0).tag(sync=True)

    def __init__(self, exercise: str, *args, **kwargs):
        super().__init__(*args, solution=SOLUTIONS[exercise], **kwargs)
    