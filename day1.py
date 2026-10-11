import cv2
import numpy as np
import random

def run_flying_particles_assembly(image_path="shailputri.jpg"):
    # Load original image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not find '{image_path}'. Make sure it is in the same folder.")
        return

    H, W, _ = img.shape

    # Interactive GUI Window
    window_name = "Navratri Day 1 - Maa Shailputri Particle Assembly"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, min(560, W), min(920, H))

    # Dot density (small bindi/points)
    step = 5  
    targets = []
    colors = []

    # Extract non-empty target points and their real colors
    for y in range(0, H, step):
        for x in range(0, W, step):
            b, g, r = img[y, x]
            targets.append((x, y))
            colors.append((int(b), int(g), int(r)))

    targets = np.array(targets, dtype=np.float32)
    colors = np.array(colors, dtype=np.uint8)
    num_particles = len(targets)

    # Spawn points flying in from all 4 outside boundaries
    starts = []
    for _ in range(num_particles):
        side = random.randint(0, 3)
        if side == 0:    # Top
            sx = random.uniform(-100, W + 100)
            sy = random.uniform(-150, -20)
        elif side == 1:  # Bottom
            sx = random.uniform(-100, W + 100)
            sy = random.uniform(H + 20, H + 150)
        elif side == 2:  # Left
            sx = random.uniform(-150, -20)
            sy = random.uniform(-100, H + 100)
        else:            # Right
            sx = random.uniform(W + 20, W + 150)
            sy = random.uniform(-100, H + 100)
        starts.append((sx, sy))

    starts = np.array(starts, dtype=np.float32)

    # Organic delay so points fly and assemble naturally
    delays = np.random.uniform(0.0, 0.4, size=num_particles).astype(np.float32)
    total_frames = 110  # Animation duration: ~3.5 to 4 seconds

    print("Particles flying in from all 4 directions... Look at the screen window!")

    for frame_idx in range(total_frames):
        canvas = np.full((H, W, 3), 246, dtype=np.uint8)

        t_global = frame_idx / float(total_frames - 1)
        t_local = (t_global - delays) / (1.0 - delays)
        t_local = np.clip(t_local, 0.0, 1.0)

        # Smooth ease-out deceleration curve
        ease_progress = 1.0 - np.power(1.0 - t_local, 3)

        # Current particle coordinates
        cur_x = starts[:, 0] + (targets[:, 0] - starts[:, 0]) * ease_progress
        cur_y = starts[:, 1] + (targets[:, 1] - starts[:, 1]) * ease_progress

        cur_xi = np.clip(cur_x.astype(np.int32), 0, W - 1)
        cur_yi = np.clip(cur_y.astype(np.int32), 0, H - 1)

        # Draw bindi / particle dots
        for i in range(num_particles):
            pt = (cur_xi[i], cur_yi[i])
            col = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
            cv2.circle(canvas, pt, 2, col, -1, cv2.LINE_AA)

        cv2.imshow(window_name, canvas)
        if cv2.waitKey(20) & 0xFF == 27:
            return

    # Seamless snap into final high-res picture
    for alpha in np.linspace(0.0, 1.0, 15):
        blended = cv2.addWeighted(img, alpha, canvas, 1.0 - alpha, 0)
        cv2.imshow(window_name, blended)
        if cv2.waitKey(20) & 0xFF == 27:
            return

    cv2.imshow(window_name, img)
    print("Assembly complete! Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_flying_particles_assembly("shailputri.jpg")