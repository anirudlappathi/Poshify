import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
//import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js';
//import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { GLTFLoader } from "./GLTFLoader.js";


const scene = new THREE.Scene();
console.log('test');
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#bg'), alpha:true
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight)
camera.position.setZ(-40);
camera.position.setX(-3);
camera.position.setY(-3);

scene.background = new THREE.Color(0xffffff);





//console.log("test2132131");

/*
let obj;
const loader = new GLTFLoader()
loader.load('scene.gltf', function (gltf) {
        obj = gltf.scene;
        scene.add(gltf.scene)
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
    },
    (error) => {
        console.log(error)
    }
)


const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(2, 2, 2);
scene.add(light);

var light1 = new THREE.AmbientLight(0xffffff);
scene.add(light1);
*/

scene.background = new THREE.Color(0x030613)

const geometry = new THREE.TorusGeometry(10, 3, 16, 100);
const material = new THREE.MeshNormalMaterial({/*color: 0x4fcdb9,*/ wireframe: false});
const torus = new THREE.Mesh(geometry, material);
scene.add(torus);

const geometry1 = new THREE.ConeGeometry( 1.62, 2.1, 8 );


let particle = new THREE.Object3D();
scene.add(particle);

for (var i = 0; i < 400; i++) 
{
    var mesh = new THREE.Mesh(geometry1, material);
    mesh.position.set(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
    mesh.position.multiplyScalar(90 + (Math.random() * 350));
    mesh.rotation.set(Math.random() * 2, Math.random() * 2, Math.random() * 2);
    particle.add(mesh);
}




const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = false;
controls.minDistance = 15;
controls.maxDistance = 50;




function animate(){
    requestAnimationFrame(animate);

    torus.rotation.x += 0.005;
    torus.rotation.y += 0.005;
    torus.rotation.z += 0.005;

    particle.rotation.x += 0.0002;
    particle.rotation.y -= 0.0040;
    
    
    controls.update();
    renderer.render(scene, camera);
}


animate();



