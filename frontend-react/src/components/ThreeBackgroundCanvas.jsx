import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { Box } from '@mui/material';

/**
 * ThreeBackgroundCanvas - Futuristic 3D geometric RAG particle mesh & glowing core.
 * Built with Three.js. Features ambient mouse parallax and dynamic glowing nodes.
 */
export default function ThreeBackgroundCanvas({ style, height = '100%', interactive = true }) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const width = container.clientWidth || window.innerWidth;
    const canvasHeight = container.clientHeight || 400;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, width / canvasHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, canvasHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 2. Central 3D Geometric RAG Mesh (Icosahedron + Wireframe)
    const coreGeometry = new THREE.IcosahedronGeometry(6, 2);
    const coreMaterial = new THREE.MeshPhongMaterial({
      color: 0x16a34a,
      emissive: 0x059669,
      emissiveIntensity: 0.35,
      wireframe: true,
      transparent: true,
      opacity: 0.45,
      shininess: 100,
    });
    const coreMesh = new THREE.Mesh(coreGeometry, coreMaterial);
    scene.add(coreMesh);

    // Inner glowing sphere
    const innerGeo = new THREE.OctahedronGeometry(3.5, 2);
    const innerMat = new THREE.MeshStandardMaterial({
      color: 0x4ade80,
      emissive: 0x22c55e,
      emissiveIntensity: 0.8,
      roughness: 0.2,
      metalness: 0.8,
      transparent: true,
      opacity: 0.7,
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    scene.add(innerMesh);

    // Outer orbital ring
    const ringGeo = new THREE.TorusGeometry(9.5, 0.12, 16, 100);
    const ringMat = new THREE.MeshStandardMaterial({
      color: 0xf97316,
      emissive: 0xea580c,
      emissiveIntensity: 0.6,
      transparent: true,
      opacity: 0.6,
    });
    const ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = Math.PI / 3;
    scene.add(ringMesh);

    // 3. Floating 3D Node Particles
    const particleCount = 120;
    const particlesGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const greenColor = new THREE.Color(0x22c55e);
    const orangeColor = new THREE.Color(0xf97316);
    const cyanColor = new THREE.Color(0x06b6d4);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 55;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 45;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 35;

      const mixedColor = i % 3 === 0 ? greenColor : i % 3 === 1 ? orangeColor : cyanColor;
      colors[i * 3] = mixedColor.r;
      colors[i * 3 + 1] = mixedColor.g;
      colors[i * 3 + 2] = mixedColor.b;
    }

    particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.65,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });
    const particleSystem = new THREE.Points(particlesGeo, particleMat);
    scene.add(particleSystem);

    // 4. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x22c55e, 3, 50);
    pointLight1.position.set(15, 15, 15);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xf97316, 2.5, 50);
    pointLight2.position.set(-15, -15, -15);
    scene.add(pointLight2);

    // 5. Mouse Interactivity & Animation Loop
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (event) => {
      if (!interactive) return;
      const rect = container.getBoundingClientRect();
      const x = event.clientX - rect.left - rect.width / 2;
      const y = event.clientY - rect.top - rect.height / 2;
      targetX = (x / rect.width) * 2;
      targetY = (y / rect.height) * 2;
    };

    if (interactive) {
      window.addEventListener('mousemove', handleMouseMove);
    }

    let animationFrameId;
    const clock = new THREE.Clock();

    const animate = () => {
      const elapsedTime = clock.getElapsedTime();

      // Smooth mouse interpolation
      mouseX += (targetX - mouseX) * 0.05;
      mouseY += (targetY - mouseY) * 0.05;

      // Rotation animations
      coreMesh.rotation.x = elapsedTime * 0.25 + mouseY * 0.5;
      coreMesh.rotation.y = elapsedTime * 0.35 + mouseX * 0.5;

      innerMesh.rotation.x = -elapsedTime * 0.4;
      innerMesh.rotation.y = -elapsedTime * 0.5;

      ringMesh.rotation.z = elapsedTime * 0.3;
      ringMesh.rotation.y = elapsedTime * 0.15;

      particleSystem.rotation.y = elapsedTime * 0.05 + mouseX * 0.2;
      particleSystem.rotation.x = elapsedTime * 0.03 + mouseY * 0.2;

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    // Handle Window Resize
    const handleResize = () => {
      if (!container) return;
      const newW = container.clientWidth;
      const newH = container.clientHeight || 400;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      if (interactive) {
        window.removeEventListener('mousemove', handleMouseMove);
      }
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      coreGeometry.dispose();
      coreMaterial.dispose();
      innerGeo.dispose();
      innerMat.dispose();
      ringGeo.dispose();
      ringMat.dispose();
      particlesGeo.dispose();
      particleMat.dispose();
      renderer.dispose();
    };
  }, [interactive]);

  return (
    <Box
      ref={containerRef}
      sx={{
        width: '100%',
        height: height,
        position: 'absolute',
        top: 0,
        left: 0,
        pointerEvents: 'none',
        overflow: 'hidden',
        zIndex: 0,
        ...style,
      }}
    />
  );
}
