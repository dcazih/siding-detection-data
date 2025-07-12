import os

def fix_label_format(label_dir):
    for fname in os.listdir(label_dir):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(label_dir, fname)
        with open(path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 6:
                continue  # skip broken or non-segment lines
            if len(parts) % 2 == 0:
                # likely duplicated class ID, remove first one
                class_id = parts[0]
                coords = parts[1:]
            else:
                class_id = parts[0]
                coords = parts[1:]

            if len(coords) % 2 != 0:
                print(f"Skipping malformed label in {fname}")
                continue

            new_line = f"{class_id} " + " ".join(coords)
            new_lines.append(new_line)

        if new_lines:
            with open(path, "w") as f:
                f.write("\n".join(new_lines) + "\n")
        else:
            print(f"Deleting empty/bad label: {fname}")
            os.remove(path)

def remove_unlabeled_images(image_dir, label_dir):
    for fname in os.listdir(image_dir):
        if not fname.endswith((".jpg", ".png", ".jpeg")):
            continue
        base = os.path.splitext(fname)[0]
        label_file = os.path.join(label_dir, base + ".txt")
        if not os.path.exists(label_file):
            print(f"Removing unlabeled image: {fname}")
            os.remove(os.path.join(image_dir, fname))

# --- Run for each split ---
splits = ["train", "valid", "test"]

for split in splits:
    fix_label_format(f"dataset2/{split}/labels")
    remove_unlabeled_images(f"dataset2/{split}/images", f"dataset2/{split}/labels")
