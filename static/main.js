import * as THREE from 'three';
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

let scene, camera, renderer;

function init() {
    // Create a scene
    scene = new THREE.Scene();

    // Create a camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 5, 10);

    // Create a renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff); // Set a light gray background color
    document.body.appendChild(renderer.domElement);

    // Add lights
    const ambientLight = new THREE.AmbientLight(0x0f0000, 2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0x000000, 0.5);
    directionalLight.position.set(0, 10, 10);
    scene.add(directionalLight);

    // Load the 3D model
    loadModel();
}

function loadModel() {

  // Create a scene, camera, renderer, etc. - Your Three.js setup

  // Define material for the spheres
  const material = new THREE.MeshStandardMaterial({
    color: 0xDEDEDE, // Base color
    metalness: 1, // Set to 1 for a fully metallic appearance
    roughness: 0, // Lower roughness for a smoother surface (0 being completely smooth)
    transparent: true, // Enable transparency
    opacity: 0.05, // Adjust opacity for transparency effect
  });

  // Ensure that the material uses reflections by enabling the reflectivity
  material.reflectivity = 1; // Adjust the reflectivity

  // Define information for the center (pistil) sphere
  const centerRadius = 1.5; // Adjust the radius for the center sphere
  const centerSegments = 128; // Number of segments for the center sphere
  const centerGeometry = new THREE.SphereGeometry(centerRadius, centerSegments, centerSegments);
  const centerMesh = new THREE.Mesh(centerGeometry, material);
  centerMesh.position.set(0, 5, 0)
  scene.add(centerMesh); // Add the center sphere to the scene

  // Define information for the petal spheres
  const petalRadius = 1.8; // Adjust the radius for the petal spheres
  const petalSegments = 128; // Number of segments for the petal spheres

  // Function to create a petal sphere
  function createPetalSphere(angle) {
    const petalGeometry = new THREE.SphereGeometry(petalRadius, petalSegments, petalSegments);
    const petalMesh = new THREE.Mesh(petalGeometry, material);

    // Calculate position based on the angle (in radians) around the center
    const posX = Math.cos(angle) * petalRadius * 1.; // Adjust the radius multiplier as needed
    const posY = Math.sin(angle) * petalRadius * 1.; // Adjust the radius multiplier as needed
    petalMesh.position.set(posX, posY + 15, 50);

    return petalMesh;
  }

  const petals = [];
  // Create four petal spheres and position them around the center
  for (let i = 0; i < 4; i++) {
    const angle = (Math.PI / 2) * i; // Angle increment to position petals evenly
    const petalMesh = createPetalSphere(angle);
    scene.add(petalMesh); // Add each petal sphere to the scene
    petals.push(petalMesh);
  }

  const whiteLight = new THREE.DirectionalLight(0xDEDEDE, 9999);
  whiteLight.position.set(500, 100, 500); // Positioned in the center
  scene.add(whiteLight);

  const whiteLight2 = new THREE.DirectionalLight(0xDEDEDE, 9999);
  whiteLight2.position.set(500, -100, 500); // Positioned in the center
  scene.add(whiteLight2);
  
  // const redLight = new THREE.DirectionalLight(0xDEDEDE, 9999);
  // redLight.position.set(-5, 100, 0); // Positioned on one side
  // scene.add(redLight);
  
  // const blueLight = new THREE.DirectionalLight(0xDEDEDE, 9999);
  // blueLight.position.set(5, 100, 0); // Positioned on the other side
  // scene.add(blueLight);



  // Render loop for animation
  function animate() {
    requestAnimationFrame(animate);

    // Rotate the petals around the center
    const time = Date.now() * 0.001; // Get current time
    const rotationSpeed = 0.2; // Adjust rotation speed as needed

    petals.forEach((petal, index) => {
        const angle = time * rotationSpeed; // Alternate rotation direction
        const petalAngle = angle + (Math.PI / 2) * index; // Offset rotation for each petal

        const posX = Math.cos(petalAngle) * petalRadius * 2; // Calculate X position
        const posY = Math.sin(petalAngle) * petalRadius * 2; // Calculate Y position

        petal.position.set(posX, posY + 5, 0); // Update petal position
    });

    // Render the scene
    renderer.render(scene, camera);
  }

  animate(); // Start the animation

}

function render() {
    // Render loop
    renderer.render(scene, camera);

    // Call render function recursively
    requestAnimationFrame(render);
}

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

init();