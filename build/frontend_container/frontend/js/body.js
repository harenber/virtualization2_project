class Body {
    constructor(texturepath, radius) {
        const geometry = new THREE.SphereGeometry(radius, 32, 32);
        const texture = new THREE.TextureLoader().load(texturepath);

        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;

        const material = new THREE.MeshPhongMaterial({map:texture});

        this.sphere = new THREE.Mesh(geometry, material);
        this.radius = radius;
        this.orbitcolor = 0x0000ff;

        this.body_prevpos = {x: 0, y: 0, z: 0}
    }

    set_prev(x, y, z) {
        this.body_prevpos = {x: x, y: y, z: z};
    }

    change_pos(x, y, z) {
        this.sphere.position.x = x;
        this.sphere.position.y = y;
        this.sphere.position.z = z;
    }

    rotate() {
        this.sphere.rotation.x += 0.05;
        this.sphere.rotation.y += 0.05;
        this.sphere.rotation.z += 0.05;
    }

    set_orbitcolor(color) {
        this.orbitcolor = color;
    }

};
