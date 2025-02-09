from flask import Flask, request, jsonify

app = Flask(__name__)

WORKOUT_DB = {
    "muscle_building": {
        "home": {
            "weeks": [
                ["Push-ups", "Pull-ups", "Bodyweight Squats", "Plank"],
                ["Dips", "Chin-ups", "Lunges", "Side Plank"],
                ["Decline Push-ups", "Inverted Rows", "Bulgarian Split Squats", "Mountain Climbers"],
                ["Pike Push-ups", "Pull-ups", "Step-ups", "Bicycle Crunches"],
                ["Diamond Push-ups", "Chin-ups", "Single-leg Squats", "Leg Raises"],
                ["Archer Push-ups", "Inverted Rows", "Pistol Squats", "Russian Twists"]
            ],
            "nutrition": {
                "bulking": ["Oatmeal with fruits", "Chicken breast with quinoa", "Greek yogurt with honey", "Salmon with sweet potatoes", "Protein shakes"],
                "cutting": ["Egg white omelette", "Grilled chicken salad", "Cottage cheese with berries", "Tuna with mixed greens", "Almonds and walnuts"]
            }
        },
        "gym": {
            "weeks": [
                ["Bench Press", "Deadlift", "Squats", "Overhead Press"],
                ["Incline Bench Press", "Pull-ups", "Leg Press", "Dumbbell Shoulder Press"],
                ["Decline Bench Press", "Barbell Rows", "Lunges", "Arnold Press"],
                ["Chest Flyes", "T-Bar Rows", "Hack Squats", "Lateral Raises"],
                ["Cable Crossovers", "Seated Rows", "Front Squats", "Rear Delt Flyes"],
                ["Pec Deck Machine", "Single-arm Dumbbell Rows", "Sumo Squats", "Shrugs"]
            ],
            "nutrition": {
                "bulking": ["Whole grain toast with avocado", "Steak with brown rice", "Protein smoothie with banana", "Grilled fish with couscous", "Mixed nuts"],
                "cutting": ["Spinach and feta omelette", "Turkey lettuce wraps", "Greek yogurt with flaxseeds", "Baked cod with asparagus", "Hummus with carrot sticks"]
            }
        }
    },
    "weight_loss": {
        "home": {
            "weeks": [
                ["Jumping Jacks", "Burpees", "Mountain Climbers", "High Knees"],
                ["Squat Jumps", "Push-ups", "Plank Jacks", "Butt Kicks"],
                ["Lunges", "Tricep Dips", "Bicycle Crunches", "Skaters"],
                ["Step-ups", "Inchworms", "Russian Twists", "Jump Rope"],
                ["Box Jumps", "Supermans", "Leg Raises", "Side Shuffles"],
                ["Tuck Jumps", "Bear Crawls", "Flutter Kicks", "Jump Squats"]
            ],
            "nutrition": ["Oatmeal with berries", "Grilled chicken with steamed vegetables", "Apple slices with peanut butter", "Quinoa salad with chickpeas", "Greek yogurt with honey"]
        },
        "gym": {
            "weeks": [
                ["Treadmill Running", "Cycling", "Elliptical Trainer", "Rowing Machine"],
                ["Stair Climber", "Jump Rope", "Battle Ropes", "Kettlebell Swings"],
                ["Boxing", "Swimming", "High-Intensity Interval Training (HIIT)", "Spin Class"],
                ["Circuit Training", "Rowing Machine", "Treadmill Sprints", "Medicine Ball Slams"],
                ["Elliptical Intervals", "Stair Sprints", "Agility Ladder Drills", "TRX Training"],
                ["Dance Cardio", "Kickboxing", "Plyometric Exercises", "Resistance Band Training"]
            ],
            "nutrition": ["Scrambled eggs with spinach", "Salmon with roasted Brussels sprouts", "Greek yogurt with almonds", "Chicken stir-fry with broccoli", "Mixed berries with cottage cheese"]
        }
    },
    "flexibility": {
        "home": {
            "weeks": [
                ["Yoga Stretches", "Dynamic Lunges", "Hip Circles", "Cat-Cow Stretch"],
                ["Hamstring Stretch", "Quad Stretch", "Shoulder Rolls", "Neck Stretch"],
                ["Child's Pose", "Seated Forward Bend", "Butterfly Stretch", "Spinal Twist"],
                ["Cobra Pose", "Downward Dog", "Pigeon Pose", "Thread the Needle"],
                ["Side Stretch", "Chest Opener", "Ankle Rotations", "Wrist Flexor Stretch"],
                ["Standing Forward Bend", "Triangle Pose", "Bridge Pose", "Happy Baby Pose"]
            ],
            "nutrition": ["Green smoothie with kale and banana", "Grilled tofu with mixed vegetables", "Lentil soup", "Chickpea salad", "Fresh fruit salad"]
        },
        "gym": {
            "weeks": [
                ["Resistance Band Stretches", "Foam Rolling", "Cable Rotations", "TRX Stretching"],
                ["Leg Press Stretch", "Lat Pulldown Stretch", "Chest Fly Stretch", "Back Extension Stretch"],
                ["Smith Machine Calf Stretch", "Preacher Curl Stretch", "Overhead Tricep Stretch", "Seated Row Stretch"],
                ["Leg Curl Stretch", "Leg Extension Stretch", "Pec Deck Stretch", "Hyperextension Stretch"],
                ["Cable Chest Stretch", "Cable Back Stretch", "Cable Shoulder Stretch", "Cable Hip Stretch"],
                ["Assisted Pull-up Stretch", "Assisted Dip Stretch", "Assisted Squat Stretch", "Assisted Lunge Stretch"]
            ],
            "nutrition": ["Avocado toast with cherry tomatoes", "Quinoa bowl with black beans", "Vegetable stir-fry with tofu", "Sweet potato and black bean salad", "Mango and pineapple smoothie"]
        }
    }
}

@app.route('/generate_workout', methods=['POST'])
def generate_workout():
    try:
        # Parse the request JSON
        user_data = request.get_json()
        if not user_data:
            return jsonify({"error": "Invalid JSON or no data provided"}), 400

        goal = user_data.get('goal')
        equipment = user_data.get('equipment')
        phase = user_data.get('phase', 'bulking')

        # Validate input
        if not goal or not equipment:
            return jsonify({"error": "Missing goal or equipment type."}), 400

        if goal not in WORKOUT_DB or equipment not in WORKOUT_DB[goal]:
            return jsonify({"error": "Invalid goal or equipment type."}), 400

        workout_plan = WORKOUT_DB[goal][equipment]["weeks"]
        
        # Nutrition fetching logic
        nutrition_plan = []
        nutrition_entry = WORKOUT_DB[goal][equipment].get("nutrition", {})

        if isinstance(nutrition_entry, dict):  # For "bulking" or "cutting" phases
            nutrition_plan = nutrition_entry.get(phase, ["Default healthy meals for this category."])
        else:
            nutrition_plan = nutrition_entry  # In cases like "weight_loss" without phases

        return jsonify({
            "goal": goal,
            "equipment": equipment,
            "phase": phase,
            "workout_plan": workout_plan,
            "nutrition_plan": nutrition_plan
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)