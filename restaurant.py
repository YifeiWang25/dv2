import json
import csv

# 如果你不想用 reverse_geocoder，可以直接把 state 设置成 "Unknown"
try:
    import reverse_geocoder as rg
    use_rg = True
except ImportError:
    print("⚠️ 没有安装 reverse_geocoder，将不会自动识别州信息。")
    use_rg = False

# 读取 JSON 文件
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for item in data:
    if "tags" in item and item["tags"].get("amenity") == "restaurant":
        lat = item.get("lat")
        lon = item.get("lon")
        name = item["tags"].get("name", "Unknown")
        cuisine = item["tags"].get("cuisine", "Unknown")

        # 如果有多个菜系（如 "chinese;japanese"），拆开
        cuisines = [c.strip() for c in cuisine.split(";")]

        # 州信息
        if use_rg and lat and lon:
            try:
                location = rg.search((lat, lon))[0]
                state = location.get("admin1", "Unknown")
            except Exception:
                state = "Unknown"
        else:
            state = "Unknown"

        for c in cuisines:
            rows.append([state, c, name])

# 写入 CSV
with open("restaurants.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["State", "Cuisine", "Name"])
    writer.writerows(rows)

print("✅ 已生成 restaurants.csv")
print("示例数据：")
for r in rows[:5]:
    print(r)