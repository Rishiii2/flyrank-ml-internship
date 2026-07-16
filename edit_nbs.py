import json
import sys

def modify_notebook(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Notebook 01
    if "01_first" in path:
        for cell in data['cells']:
            if cell.get('source') and len(cell['source']) > 0 and "# Your discovery here" in cell['source'][0]:
                cell['source'] = [
                    "# Redo Discovery A but only for pages with impressions_90d > 0\n",
                    "visible_only = df[df['impressions_90d'] > 0]\n",
                    "corr_visible = visible_only['search_volume'].corr(visible_only['impressions_90d'])\n",
                    "print(f\"Correlation between search_volume and impressions_90d for visible pages: {corr_visible:.3f}\")\n",
                    "print(\"Even for visible pages, search volume barely predicts traffic.\")\n"
                ]
                break
    elif "02_your" in path:
        for cell in data['cells']:
            if cell.get('source') and len(cell['source']) > 0 and "# Your rule here" in cell['source'][0]:
                cell['source'] = [
                    "# Simple rule: position_tier <= 3 and ctr < 0.05\n",
                    "def my_rule(row):\n",
                    "    if row['position_tier'] <= 3 and row['ctr'] < 0.05:\n",
                    "        return 1\n",
                    "    return 0\n",
                    "\n",
                    "df['my_rule_prediction'] = df.apply(my_rule, axis=1)\n",
                    "my_rule_precision = df[df['my_rule_prediction'] == 1]['trend_direction'].apply(lambda x: 1 if x == 'down' else 0).mean()\n",
                    "print(f\"My Rule Precision: {my_rule_precision:.3f}\")\n"
                ]
                break
                
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)

if __name__ == "__main__":
    modify_notebook(sys.argv[1])
