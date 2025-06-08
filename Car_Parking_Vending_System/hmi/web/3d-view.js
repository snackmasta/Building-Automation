// 3D Parking Visualization using Three.js

class Parking3DView {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.parkingStructure = null;
        this.vehicles = new Map();
        this.elevators = [];
        this.isInitialized = false;
        
        this.settings = {
            levelHeight: 3.0,
            spaceWidth: 2.5,
            spaceLength: 5.0,
            spacesPerRow: 10,
            buildingWidth: 50,
            buildingDepth: 25,
            totalLevels: 15
        };
        
        this.materials = {
            building: null,
            available: null,
            occupied: null,
            reserved: null,
            maintenance: null,
            elevator: null,
            vehicle: null
        };
        
        this.colors = {
            building: 0x808080,
            available: 0x27ae60,
            occupied: 0xe74c3c,
            reserved: 0xf39c12,
            maintenance: 0x6c757d,
            elevator: 0x3498db,
            vehicle: 0x2c3e50,
            ground: 0x34495e,
            sky: 0x87ceeb
        };
    }

    initialize(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('3D container not found:', containerId);
            return false;
        }

        try {
            this.setupRenderer(container);
            this.setupScene();
            this.setupCamera();
            this.setupControls();
            this.setupLighting();
            this.createMaterials();
            this.createParkingStructure();
            this.createElevators();
            this.setupEventListeners();
            this.startRenderLoop();
            
            this.isInitialized = true;
            console.log('3D parking view initialized successfully');
            return true;
        } catch (error) {
            console.error('Failed to initialize 3D view:', error);
            return false;
        }
    }

    setupRenderer(container) {
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true 
        });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.setClearColor(this.colors.sky, 1);
        
        container.appendChild(this.renderer.domElement);
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.Fog(this.colors.sky, 50, 200);
        
        // Add ground plane
        const groundGeometry = new THREE.PlaneGeometry(200, 200);
        const groundMaterial = new THREE.MeshLambertMaterial({ color: this.colors.ground });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    setupCamera() {
        this.camera = new THREE.PerspectiveCamera(
            60,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        this.camera.position.set(60, 40, 60);
        this.camera.lookAt(0, 20, 0);
    }

    setupControls() {
        // Simple orbit controls implementation
        this.controls = {
            enabled: true,
            target: new THREE.Vector3(0, 20, 0),
            minDistance: 20,
            maxDistance: 150,
            minPolarAngle: 0,
            maxPolarAngle: Math.PI / 2.2,
            autoRotate: false,
            autoRotateSpeed: 0.5
        };
        
        this.setupMouseControls();
    }

    setupMouseControls() {
        let isMouseDown = false;
        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;
        
        const canvas = this.renderer.domElement;
        
        canvas.addEventListener('mousedown', (event) => {
            isMouseDown = true;
            mouseX = event.clientX;
            mouseY = event.clientY;
        });
        
        canvas.addEventListener('mousemove', (event) => {
            if (!isMouseDown) return;
            
            const deltaX = event.clientX - mouseX;
            const deltaY = event.clientY - mouseY;
            
            targetX += deltaX * 0.01;
            targetY += deltaY * 0.01;
            
            mouseX = event.clientX;
            mouseY = event.clientY;
        });
        
        canvas.addEventListener('mouseup', () => {
            isMouseDown = false;
        });
        
        canvas.addEventListener('wheel', (event) => {
            const distance = this.camera.position.distanceTo(this.controls.target);
            const newDistance = Math.max(
                this.controls.minDistance,
                Math.min(this.controls.maxDistance, distance + event.deltaY * 0.1)
            );
            
            const direction = new THREE.Vector3()
                .subVectors(this.camera.position, this.controls.target)
                .normalize();
            
            this.camera.position.copy(
                this.controls.target.clone().add(direction.multiplyScalar(newDistance))
            );
        });
        
        // Auto-rotate camera
        setInterval(() => {
            if (this.controls.autoRotate) {
                targetX += this.controls.autoRotateSpeed * 0.01;
            }
            
            const radius = this.camera.position.distanceTo(this.controls.target);
            this.camera.position.x = this.controls.target.x + radius * Math.cos(targetX) * Math.sin(targetY + Math.PI/4);
            this.camera.position.z = this.controls.target.z + radius * Math.sin(targetX) * Math.sin(targetY + Math.PI/4);
            this.camera.position.y = this.controls.target.y + radius * Math.cos(targetY + Math.PI/4);
            this.camera.lookAt(this.controls.target);
        }, 16);
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        // Directional light (sun)
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 100, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 200;
        directionalLight.shadow.camera.left = -100;
        directionalLight.shadow.camera.right = 100;
        directionalLight.shadow.camera.top = 100;
        directionalLight.shadow.camera.bottom = -100;
        this.scene.add(directionalLight);
        
        // Additional point lights for interior
        for (let level = 1; level <= this.settings.totalLevels; level++) {
            const pointLight = new THREE.PointLight(0xffffff, 0.3, 30);
            pointLight.position.set(0, level * this.settings.levelHeight, 0);
            this.scene.add(pointLight);
        }
    }

    createMaterials() {
        this.materials.building = new THREE.MeshLambertMaterial({ 
            color: this.colors.building,
            transparent: true,
            opacity: 0.8
        });
        
        this.materials.available = new THREE.MeshLambertMaterial({ 
            color: this.colors.available,
            emissive: this.colors.available,
            emissiveIntensity: 0.1
        });
        
        this.materials.occupied = new THREE.MeshLambertMaterial({ 
            color: this.colors.occupied,
            emissive: this.colors.occupied,
            emissiveIntensity: 0.1
        });
        
        this.materials.reserved = new THREE.MeshLambertMaterial({ 
            color: this.colors.reserved,
            emissive: this.colors.reserved,
            emissiveIntensity: 0.1
        });
        
        this.materials.maintenance = new THREE.MeshLambertMaterial({ 
            color: this.colors.maintenance
        });
        
        this.materials.elevator = new THREE.MeshLambertMaterial({ 
            color: this.colors.elevator,
            emissive: this.colors.elevator,
            emissiveIntensity: 0.2
        });
        
        this.materials.vehicle = new THREE.MeshLambertMaterial({ 
            color: this.colors.vehicle
        });
    }

    createParkingStructure() {
        this.parkingStructure = new THREE.Group();
        
        // Create building frame
        this.createBuildingFrame();
        
        // Create parking spaces for each level
        for (let level = 1; level <= this.settings.totalLevels; level++) {
            this.createParkingLevel(level);
        }
        
        this.scene.add(this.parkingStructure);
    }

    createBuildingFrame() {
        // Create building skeleton
        const frameGroup = new THREE.Group();
        
        // Vertical columns
        const columnGeometry = new THREE.BoxGeometry(0.5, this.settings.totalLevels * this.settings.levelHeight, 0.5);
        const columnPositions = [
            [-this.settings.buildingWidth/2, 0, -this.settings.buildingDepth/2],
            [this.settings.buildingWidth/2, 0, -this.settings.buildingDepth/2],
            [-this.settings.buildingWidth/2, 0, this.settings.buildingDepth/2],
            [this.settings.buildingWidth/2, 0, this.settings.buildingDepth/2]
        ];
        
        columnPositions.forEach(pos => {
            const column = new THREE.Mesh(columnGeometry, this.materials.building);
            column.position.set(pos[0], pos[1] + (this.settings.totalLevels * this.settings.levelHeight) / 2, pos[2]);
            column.castShadow = true;
            frameGroup.add(column);
        });
        
        // Floor slabs
        const floorGeometry = new THREE.BoxGeometry(
            this.settings.buildingWidth, 
            0.2, 
            this.settings.buildingDepth
        );
        
        for (let level = 0; level <= this.settings.totalLevels; level++) {
            const floor = new THREE.Mesh(floorGeometry, this.materials.building);
            floor.position.y = level * this.settings.levelHeight;
            floor.receiveShadow = true;
            frameGroup.add(floor);
        }
        
        this.parkingStructure.add(frameGroup);
    }

    createParkingLevel(level) {
        const levelGroup = new THREE.Group();
        levelGroup.name = `level_${level}`;
        
        const y = (level - 1) * this.settings.levelHeight + 0.1;
        
        // Create parking spaces (20 spaces per level, 10 per side)
        for (let side = 0; side < 2; side++) {
            for (let space = 0; space < this.settings.spacesPerRow; space++) {
                const spaceId = `${level}-${side * this.settings.spacesPerRow + space + 1}`;
                const spaceIndicator = this.createParkingSpace(spaceId, level, space, side);
                spaceIndicator.position.set(
                    (space - this.settings.spacesPerRow/2 + 0.5) * this.settings.spaceWidth,
                    y,
                    (side === 0 ? -1 : 1) * this.settings.spaceLength
                );
                levelGroup.add(spaceIndicator);
            }
        }
        
        this.parkingStructure.add(levelGroup);
    }

    createParkingSpace(spaceId, level, space, side) {
        const spaceGeometry = new THREE.BoxGeometry(
            this.settings.spaceWidth * 0.8, 
            0.1, 
            this.settings.spaceLength * 0.8
        );
        
        const spaceIndicator = new THREE.Mesh(spaceGeometry, this.materials.available);
        spaceIndicator.name = spaceId;
        spaceIndicator.userData = {
            spaceId: spaceId,
            level: level,
            space: space,
            side: side,
            status: 'available'
        };
        
        return spaceIndicator;
    }

    createElevators() {
        const elevatorPositions = [
            { x: -20, z: 0 },
            { x: 0, z: 0 },
            { x: 20, z: 0 }
        ];
        
        elevatorPositions.forEach((pos, index) => {
            const elevator = this.createElevator(index + 1, pos.x, pos.z);
            this.elevators.push(elevator);
            this.scene.add(elevator);
        });
    }

    createElevator(id, x, z) {
        const elevatorGroup = new THREE.Group();
        elevatorGroup.name = `elevator_${id}`;
        
        // Elevator shaft
        const shaftGeometry = new THREE.BoxGeometry(3, this.settings.totalLevels * this.settings.levelHeight, 3);
        const shaft = new THREE.Mesh(shaftGeometry, this.materials.elevator);
        shaft.position.set(x, (this.settings.totalLevels * this.settings.levelHeight) / 2, z);
        shaft.material.transparent = true;
        shaft.material.opacity = 0.3;
        elevatorGroup.add(shaft);
        
        // Elevator car
        const carGeometry = new THREE.BoxGeometry(2.5, 0.5, 2.5);
        const car = new THREE.Mesh(carGeometry, this.materials.elevator);
        car.position.set(x, this.settings.levelHeight, z);
        car.castShadow = true;
        car.name = `elevator_car_${id}`;
        elevatorGroup.add(car);
        
        return elevatorGroup;
    }

    updateParkingSpace(spaceId, status, vehicleData = null) {
        if (!this.isInitialized) return;
        
        const spaceIndicator = this.scene.getObjectByName(spaceId);
        if (!spaceIndicator) return;
        
        // Update space material based on status
        switch (status) {
            case 'available':
                spaceIndicator.material = this.materials.available;
                break;
            case 'occupied':
                spaceIndicator.material = this.materials.occupied;
                break;
            case 'reserved':
                spaceIndicator.material = this.materials.reserved;
                break;
            case 'maintenance':
                spaceIndicator.material = this.materials.maintenance;
                break;
        }
        
        spaceIndicator.userData.status = status;
        
        // Add or remove vehicle
        if (status === 'occupied' && vehicleData) {
            this.addVehicle(spaceId, vehicleData);
        } else {
            this.removeVehicle(spaceId);
        }
    }

    addVehicle(spaceId, vehicleData) {
        const spaceIndicator = this.scene.getObjectByName(spaceId);
        if (!spaceIndicator) return;
        
        // Remove existing vehicle if any
        this.removeVehicle(spaceId);
        
        // Create vehicle model
        const vehicleGeometry = new THREE.BoxGeometry(1.8, 0.8, 4.2);
        const vehicle = new THREE.Mesh(vehicleGeometry, this.materials.vehicle);
        
        vehicle.position.copy(spaceIndicator.position);
        vehicle.position.y += 0.5;
        vehicle.name = `vehicle_${spaceId}`;
        vehicle.castShadow = true;
        
        this.vehicles.set(spaceId, vehicle);
        this.scene.add(vehicle);
    }

    removeVehicle(spaceId) {
        const vehicle = this.vehicles.get(spaceId);
        if (vehicle) {
            this.scene.remove(vehicle);
            this.vehicles.delete(spaceId);
        }
    }

    updateElevatorPosition(elevatorId, level) {
        if (!this.isInitialized) return;
        
        const elevator = this.scene.getObjectByName(`elevator_${elevatorId}`);
        if (!elevator) return;
        
        const car = elevator.getObjectByName(`elevator_car_${elevatorId}`);
        if (!car) return;
        
        // Animate elevator movement
        const targetY = (level - 1) * this.settings.levelHeight + 0.5;
        
        // Simple animation
        const animate = () => {
            const currentY = car.position.y;
            const diff = targetY - currentY;
            
            if (Math.abs(diff) > 0.1) {
                car.position.y += diff * 0.1;
                requestAnimationFrame(animate);
            } else {
                car.position.y = targetY;
            }
        };
        
        animate();
    }

    focusOnLevel(level) {
        if (!this.isInitialized) return;
        
        const targetY = (level - 1) * this.settings.levelHeight + 5;
        
        // Animate camera to focus on specific level
        const animate = () => {
            const currentY = this.camera.position.y;
            const diff = targetY - currentY;
            
            if (Math.abs(diff) > 0.5) {
                this.camera.position.y += diff * 0.1;
                this.controls.target.y += diff * 0.1;
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }

    setAutoRotate(enabled) {
        this.controls.autoRotate = enabled;
    }

    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.onWindowResize();
        });
        
        // Click interaction
        this.renderer.domElement.addEventListener('click', (event) => {
            this.onMouseClick(event);
        });
    }

    onWindowResize() {
        if (!this.isInitialized) return;
        
        const container = this.renderer.domElement.parentElement;
        this.camera.aspect = container.clientWidth / container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(container.clientWidth, container.clientHeight);
    }

    onMouseClick(event) {
        if (!this.isInitialized) return;
        
        const rect = this.renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((event.clientX - rect.left) / rect.width) * 2 - 1,
            -((event.clientY - rect.top) / rect.height) * 2 + 1
        );
        
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);
        
        const intersects = raycaster.intersectObjects(this.scene.children, true);
        
        if (intersects.length > 0) {
            const object = intersects[0].object;
            if (object.userData.spaceId) {
                this.onSpaceClick(object.userData);
            }
        }
    }

    onSpaceClick(spaceData) {
        console.log('Space clicked:', spaceData);
        
        // Emit custom event for space selection
        const event = new CustomEvent('spaceSelected', {
            detail: spaceData
        });
        document.dispatchEvent(event);
    }

    startRenderLoop() {
        const animate = () => {
            requestAnimationFrame(animate);
            
            if (this.isInitialized) {
                this.renderer.render(this.scene, this.camera);
            }
        };
        
        animate();
    }

    updateParkingData(parkingData) {
        if (!this.isInitialized) return;
        
        if (parkingData.spaces) {
            parkingData.spaces.forEach(space => {
                this.updateParkingSpace(space.id, space.status, space.vehicle);
            });
        }
    }

    updateElevatorData(elevatorData) {
        if (!this.isInitialized) return;
        
        if (elevatorData.elevators) {
            elevatorData.elevators.forEach(elevator => {
                this.updateElevatorPosition(elevator.id, elevator.level);
            });
        }
    }

    dispose() {
        if (this.isInitialized) {
            this.renderer.dispose();
            this.scene.clear();
            this.vehicles.clear();
            this.elevators.length = 0;
            this.isInitialized = false;
        }
    }

    exportImage(format = 'png') {
        if (!this.isInitialized) return null;
        
        this.renderer.render(this.scene, this.camera);
        return this.renderer.domElement.toDataURL(`image/${format}`);
    }

    getStats() {
        if (!this.isInitialized) return null;
        
        return {
            objects: this.scene.children.length,
            vehicles: this.vehicles.size,
            elevators: this.elevators.length,
            triangles: this.renderer.info.render.triangles,
            calls: this.renderer.info.render.calls
        };
    }
}

// Initialize 3D view when needed
function initialize3DView() {
    if (!window.parking3D) {
        window.parking3D = new Parking3DView();
        
        const success = window.parking3D.initialize('parking3D');
        if (success) {
            console.log('3D parking view initialized');
            
            // Listen for space selection events
            document.addEventListener('spaceSelected', (event) => {
                console.log('Space selected in 3D view:', event.detail);
                // Handle space selection
            });
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Parking3DView;
} else {
    window.Parking3DView = Parking3DView;
    window.initialize3DView = initialize3DView;
}
