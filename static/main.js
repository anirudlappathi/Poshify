var renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var onRenderFcts = [];
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(25, window.innerWidth / window.innerHeight, 0.01, 1000);
camera.position.z = 15;
camera.position.y = 8;

// Red ambient light
var redAmbientLight = new THREE.AmbientLight(0xff0000, 0.01);
scene.add(redAmbientLight);

// Blue ambient light
var blueAmbientLight = new THREE.AmbientLight(0x0000ff, 0.01);
scene.add(blueAmbientLight);

scene.fog = new THREE.Fog(0x000, 0, 45);

// ... Lights and other setup ...
var geometry = new THREE.TorusGeometry(3, 1, 16, 100);
var material = new THREE.MeshPhongMaterial({
  color: 0x996633, // A neutral color (brownish)
  specular: 0x050505, // Set the specular highlight color (dark)
  shininess: 100, // Increase shininess for a glossy effect
  side: THREE.DoubleSide,
  emissive: 0x000000, // Set emissive color (black)
  emissiveIntensity: 0.1 // Low intensity for slight emissive effect
});

var mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

mesh.rotation.y = Math.PI / 4;
mesh.rotation.x = Math.PI / 4;
mesh.rotation.z = Math.PI / 4;

mesh.scale.set(0.4, 0.4, 0.4);

mesh.position.y = 8;

var xRotationSpeed = 0.2; // Original x rotation speed
var yRotationSpeed = 0.2; // Original y rotation speed
var zRotationSpeed = 0.2; // Original z rotation speed

var initialSpeed = 5; // Initial speed multiplier
var initialSpinTime = 0;

var increaseFactor = 0.5; // Adjust this factor as needed

// Function to handle scroll events
function handleScroll(event) {
  currentRotationSpeed += 0.5
}

// Add a scroll event listener
window.addEventListener('wheel', handleScroll);


// Modify the rotation in the render loop
var initialRotationSpeed = 20.0; // Initial fast rotation speed
var decelerationFactor = 0.99; // Factor to slow down the rotation speed
var currentRotationSpeed = initialRotationSpeed;

var initialSpinDuration = 300; // 0.3 seconds
var spinTimer = initialSpinDuration;

onRenderFcts.push(function(delta, now) {
  if (spinTimer >= 0) {
    mesh.rotation.y += currentRotationSpeed * delta;
    spinTimer -= delta * 1000;
    currentRotationSpeed *= decelerationFactor; // Apply deceleration
  } else {
    mesh.rotation.y += currentRotationSpeed * delta;
    if (currentRotationSpeed > 0.2)
      currentRotationSpeed *= decelerationFactor; // Continuously slow down
  }
  renderer.render(scene, camera);
});


var lastTimeMsec = null;
requestAnimationFrame(function animate(nowMsec) {
  requestAnimationFrame(animate);
  lastTimeMsec = lastTimeMsec || nowMsec - 1000 / 60;
  var deltaMsec = Math.min(200, nowMsec - lastTimeMsec);
  lastTimeMsec = nowMsec;
  onRenderFcts.forEach(function(onRenderFct) {
    onRenderFct(deltaMsec / 1000, nowMsec / 1000);
  });
});
