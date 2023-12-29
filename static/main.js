import * as THREE from "https://unpkg.com/three@0.127/build/three.module.js";
import * as dat from "https://unpkg.com/three@0.127/examples/jsm/libs/dat.gui.module.js";
import Stats from "https://unpkg.com/three@0.127/examples/jsm/libs/stats.module.js";
import { OrbitControls } from "https://unpkg.com/three@0.127/examples/jsm/controls/OrbitControls.js";

const stats = new Stats();
const gui = new dat.GUI();
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
const renderer = new THREE.WebGLRenderer({ antialias: true });
const controls = new OrbitControls(camera, renderer.domElement);

camera.position.set(3, -2, 3);
renderer.shadowMap.enabled = true;
controls.enableDamping = true;
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
controls.enablePan = false;
controls.maxDistance = 50;
controls.autoRotate = true;
controls.autoRotateSpeed = 3;

// Set the background color to white
renderer.setClearColor(0xffffff);

document.body.style.margin = 0;
document.body.appendChild(renderer.domElement);
document.body.appendChild(stats.dom);



const defaultGuiConfig = {
  radomColors: false,
  color: 0xffffff,
  size: 0.015,
  radius: 1,
  tube: 0.5,
  radialSegments: 32,
  tubularSegments: 128,
  reset: () => {
    guiConfig = { ...defaultGuiConfig };
    gui.remember(guiConfig);
    reCreateGeo();
  }
};

const guiConfig = { ...defaultGuiConfig };

let donutGeo, donutMat, donut;

const createDonut = () => {
  if (donut != null) {
    donutGeo.dispose();
    donutMat.dispose();
    scene.remove(donut);
  }

  const {
    radius,
    tube,
    radialSegments,
    tubularSegments,
    radomColors
  } = guiConfig;

  donutGeo = new THREE.TorusGeometry(
    radius,
    tube,
    radialSegments,
    tubularSegments
  );
  donutMat = new THREE.PointsMaterial({
    color: 0x000000, // Set particle color to black
    size: guiConfig.size,
    sizeAttenuation: true
  });

  if (radomColors) {
    const pointsCount = donutGeo.attributes.position.count;
    const colors = new Float32Array(pointsCount * 3);

    for (let i = 0; i < pointsCount; i++) {
      colors[i * 3] = Math.random();
      colors[i * 3 + 1] = Math.random();
      colors[i * 3 + 2] = Math.random();
    }

    donutGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    donutMat.vertexColors = true;
  }

  donut = new THREE.Points(donutGeo, donutMat);
  scene.add(donut);
};

createDonut();

const animate = () => {
  stats.begin();

  controls.update();
  renderer.render(scene, camera);
  // donut.rotation.y += 0.005;
  // donut.rotation.x += 0.005;

  stats.end();
  requestAnimationFrame(animate);
};

animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
