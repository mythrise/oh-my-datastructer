/**
 * OMD Three.js 可视化框架
 *
 * 通用 3D 渲染引擎，由 /ds:visualize 根据数据结构类型填充具体渲染逻辑。
 * 支持模式: tree, graph, sort, hash, string
 */

/* ===== 全局状态 ===== */
let scene, camera, renderer, controls;
let raycaster, mouse;
let interactiveObjects = [];
let showLabels = true;
let animationRunning = false;

/* ===== 颜色常量 ===== */
const COLORS = {
    CYBER_CYAN: 0x00f3ff,
    NEON_PURPLE: 0xa855f7,
    NEON_PINK: 0xff006e,
    SUCCESS: 0x00ff88,
    WARNING: 0xffaa00,
    DANGER: 0xff4444,
    BG: 0x0a0a0f,
    NODE_DEFAULT: 0x00f3ff,
    NODE_HOVER: 0xa855f7,
    NODE_SELECTED: 0xff006e,
    EDGE_DEFAULT: 0x444466,
};

/* ===== 场景初始化 ===== */
function initScene() {
    const container = document.getElementById("canvas-container");
    const w = window.innerWidth;
    const h = window.innerHeight;

    // 场景
    scene = new THREE.Scene();
    scene.background = new THREE.Color(COLORS.BG);
    scene.fog = new THREE.FogExp2(COLORS.BG, 0.003);

    // 相机
    camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);
    camera.position.set(0, 10, 20);

    // 渲染器
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.appendChild(renderer.domElement);

    // 控制器
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 3;
    controls.maxDistance = 100;

    // 光照
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const pointLight = new THREE.PointLight(COLORS.CYBER_CYAN, 1, 100);
    pointLight.position.set(10, 20, 10);
    scene.add(pointLight);

    // Raycaster
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // 事件
    window.addEventListener("resize", onResize);
    renderer.domElement.addEventListener("click", onInteract);
    renderer.domElement.addEventListener("mousemove", onHover);

    // 根据数据类型渲染
    if (VIZ_DATA) {
        buildVisualization(VIZ_DATA);
        updateHUD(VIZ_DATA);
    }

    animate();
}

/* ===== 根据数据类型分发渲染 ===== */
function buildVisualization(data) {
    const mode = data.metadata?.viz_mode || "tree";

    switch (mode) {
        case "tree":
            buildTreeVisualization(data);
            break;
        case "graph":
            buildGraphVisualization(data);
            break;
        case "sort":
            buildSortVisualization(data);
            break;
        case "hash":
            buildHashVisualization(data);
            break;
        case "string":
            buildStringVisualization(data);
            break;
        default:
            console.warn(`[OMD] Unknown viz mode: ${mode}, falling back to tree`);
            buildTreeVisualization(data);
    }
}

/* ===== 树形渲染（默认实现） ===== */
function buildTreeVisualization(data) {
    // 由 /ds:visualize 根据具体树结构填充
    // 基础框架：递归遍历节点，创建球体 + 连线
    const nodes = data.tree?.nodes || [];
    const edges = data.tree?.edges || [];

    nodes.forEach(node => {
        const geometry = new THREE.SphereGeometry(0.3, 16, 16);
        const material = new THREE.MeshPhongMaterial({
            color: COLORS.NODE_DEFAULT,
            emissive: COLORS.CYBER_CYAN,
            emissiveIntensity: 0.2,
            transparent: true,
            opacity: 0.9,
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(node.x || 0, node.y || 0, node.z || 0);
        mesh.userData = node;
        scene.add(mesh);
        interactiveObjects.push(mesh);
    });

    edges.forEach(edge => {
        const from = nodes.find(n => n.id === edge.from);
        const to = nodes.find(n => n.id === edge.to);
        if (from && to) {
            const points = [
                new THREE.Vector3(from.x, from.y, from.z || 0),
                new THREE.Vector3(to.x, to.y, to.z || 0),
            ];
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: COLORS.EDGE_DEFAULT, transparent: true, opacity: 0.6 });
            scene.add(new THREE.Line(geometry, material));
        }
    });
}

/* ===== 占位渲染器 — 由 /ds:visualize 实现 ===== */
function buildGraphVisualization(data) { console.log("[OMD] Graph viz — to be implemented by /ds:visualize"); }
function buildSortVisualization(data)  { console.log("[OMD] Sort viz — to be implemented by /ds:visualize"); }
function buildHashVisualization(data)  { console.log("[OMD] Hash viz — to be implemented by /ds:visualize"); }
function buildStringVisualization(data){ console.log("[OMD] String viz — to be implemented by /ds:visualize"); }

/* ===== HUD 更新 ===== */
function updateHUD(data) {
    const meta = data.metadata || {};
    document.getElementById("ds-type").textContent = meta.ds_type || "—";
    document.getElementById("algo-name").textContent = meta.algorithm || "—";
    document.getElementById("data-size").textContent = meta.data_size || "—";

    // 统计面板
    const statsContainer = document.getElementById("stats-container");
    const metrics = data.metrics || {};
    statsContainer.innerHTML = "";
    Object.entries(metrics).forEach(([key, val]) => {
        const div = document.createElement("div");
        div.className = "stat-item";
        div.innerHTML = `<span class="stat-label">${key}</span><span class="stat-value">${val}</span>`;
        statsContainer.appendChild(div);
    });
}

/* ===== 交互 ===== */
function onInteract(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(interactiveObjects);

    if (hits.length > 0) {
        const obj = hits[0].object;
        showDetail(obj.userData);
    }
}

function onHover(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(interactiveObjects);

    interactiveObjects.forEach(o => {
        o.material.emissiveIntensity = 0.2;
        o.scale.setScalar(1);
    });

    if (hits.length > 0) {
        hits[0].object.material.emissiveIntensity = 0.6;
        hits[0].object.scale.setScalar(1.3);
        renderer.domElement.style.cursor = "pointer";
    } else {
        renderer.domElement.style.cursor = "default";
    }
}

function showDetail(data) {
    const panel = document.getElementById("detail-panel");
    const content = document.getElementById("detail-content");
    panel.style.display = "block";

    content.innerHTML = "";
    Object.entries(data).forEach(([key, val]) => {
        if (key === "x" || key === "y" || key === "z") return;
        const div = document.createElement("div");
        div.className = "detail-row";
        div.textContent = `${key}: ${typeof val === "object" ? JSON.stringify(val) : val}`;
        content.appendChild(div);
    });
}

/* ===== 控制按钮 ===== */
function resetCamera() {
    camera.position.set(0, 10, 20);
    controls.target.set(0, 0, 0);
    controls.update();
}

function toggleLabels() {
    showLabels = !showLabels;
    // 由具体实现处理标签显隐
}

function toggleAnimation() {
    animationRunning = !animationRunning;
}

/* ===== 渲染循环 ===== */
function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
