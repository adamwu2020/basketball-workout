import random
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

WORKOUTS = {
    "shooting": {
        "label": "Shooting",
        "icon": "🏀",
        "subcategories": {
            "free_throw": {
                "label": "Free Throw",
                "instructions": [
                    "Stand at the free throw line with feet shoulder-width apart.",
                    "Hold the ball with your dominant hand under the ball and guide hand on the side.",
                    "Bend your knees slightly and align your shooting elbow with the basket.",
                    "Take a deep breath, focus on the back of the rim.",
                    "Push up smoothly, extending your legs and arm simultaneously.",
                    "Flick your wrist at the top — follow through with fingers pointing down.",
                    "Shoot 50 free throws. Track how many you make. Rest 30 seconds between sets of 10.",
                ],
                "duration": "20 minutes",
                "reps": "50 shots (5 sets of 10)",
                "focus": "Consistency and muscle memory",
            },
            "3_point": {
                "label": "3-Point Shots",
                "instructions": [
                    "Start at the left corner three-point line.",
                    "Square your feet and hips toward the basket before catching or picking up the ball.",
                    "Use a 1-2 step or hop step to generate upward momentum.",
                    "Keep the ball high on your shot pocket — no dipping below your waist.",
                    "Jump straight up, release at the peak of your jump.",
                    "Follow through fully — hold your wrist until the ball hits the net.",
                    "Move through 5 spots: left corner, left wing, top of the arc, right wing, right corner. Shoot 5 at each spot.",
                ],
                "duration": "25 minutes",
                "reps": "25 shots (5 per spot)",
                "focus": "Arc, balance, and consistent release point",
            },
            "mid_range": {
                "label": "Mid-Range Shot",
                "instructions": [
                    "Pick a spot in the mid-range area (elbow, baseline, or wing).",
                    "Simulate catching off a pass — step into your shot with balance.",
                    "Keep your eyes on the target early — pick up the rim as soon as possible.",
                    "Maintain a low, stable base with a slight forward lean.",
                    "Drive your shooting hand straight up through the ball.",
                    "Hold your follow-through until the ball hits the rim.",
                    "Work the mid-range elbow-to-elbow drill: shoot from the right elbow, sprint to left elbow, repeat for 4 sets.",
                ],
                "duration": "20 minutes",
                "reps": "40 shots (elbow-to-elbow, 4 sets of 10)",
                "focus": "Footwork, balance, and soft touch",
            },
        },
    },
    "conditioning": {
        "label": "Conditioning",
        "icon": "⚡",
        "subcategories": {
            "sprints": {
                "label": "Sprints",
                "instructions": [
                    "Start at the baseline. Get into an athletic stance — low hips, weight on the balls of your feet.",
                    "Sprint at full speed to the opposite baseline.",
                    "Touch the line with your hand, then sprint back.",
                    "That is one full-court suicide. Rest 20 seconds.",
                    "Complete 10 full-court suicides total.",
                    "For the last 2 reps, push yourself to beat your fastest time.",
                    "Cool down with a 2-minute light jog around the court.",
                ],
                "duration": "20 minutes",
                "reps": "10 full-court suicides",
                "focus": "Acceleration, endurance, and mental toughness",
            },
            "defensive_slides": {
                "label": "Defensive Slides",
                "instructions": [
                    "Get into a defensive stance: feet wide, hips low, arms out.",
                    "Never cross your feet — always slide step laterally.",
                    "Start at the left sideline, slide to the right sideline, then back.",
                    "Stay low the entire time — no popping up between slides.",
                    "Drive your lead foot out and push off your back foot hard.",
                    "Keep your eyes up as if guarding a ball handler.",
                    "Complete 8 sideline-to-sideline trips. Rest 30 seconds between each pair.",
                ],
                "duration": "15 minutes",
                "reps": "8 sideline-to-sideline trips",
                "focus": "Lateral quickness, low center of gravity, and defensive positioning",
            },
            "weights": {
                "label": "Weights",
                "instructions": [
                    "Warm up with 5 minutes of light cardio or dynamic stretching.",
                    "Squats (3 sets x 10 reps): feet shoulder-width apart, lower until thighs are parallel to the floor.",
                    "Romanian Deadlifts (3 sets x 10 reps): hinge at the hips, keep your back flat, feel the hamstring stretch.",
                    "Lateral lunges (3 sets x 8 reps per leg): step wide to the side, sit into that hip, keep the other leg straight.",
                    "Box jumps (3 sets x 8 reps): explode up, land softly with bent knees.",
                    "Calf raises (3 sets x 15 reps): stand on the edge of a step, lower fully, raise fully.",
                    "Rest 60–90 seconds between sets. Prioritize form over heavy weight.",
                ],
                "duration": "45 minutes",
                "reps": "3 sets per exercise",
                "focus": "Lower body strength and explosive power",
            },
        },
    },
    "ball_handling": {
        "label": "Ball Handling",
        "icon": "🔄",
        "subcategories": {
            "pound_dribbles": {
                "label": "Pound Dribbles",
                "instructions": [
                    "Stand in an athletic stance, feet shoulder-width apart, knees bent.",
                    "Dribble the ball as hard as possible straight down — pound it into the floor.",
                    "Keep your eyes up, do not look at the ball.",
                    "Right hand only: 30 seconds of hard pound dribbles.",
                    "Left hand only: 30 seconds of hard pound dribbles.",
                    "Alternate hands every dribble: 30 seconds.",
                    "Move through low (ball below knee), mid (waist height), and high dribble positions — 30 seconds each. Repeat the circuit 3 times.",
                ],
                "duration": "15 minutes",
                "reps": "3 full circuits",
                "focus": "Hand strength, ball control, and keeping your eyes up",
            },
            "figure_eights": {
                "label": "Figure Eights",
                "instructions": [
                    "Stand with feet wider than shoulder-width, knees deeply bent.",
                    "Pass the ball around your right leg from front to back, then transfer to your left hand.",
                    "Pass around the left leg from back to front, then transfer to your right hand.",
                    "This creates a figure-eight pattern through your legs.",
                    "Start slow to build the pattern, then speed up progressively.",
                    "Do 30 seconds in one direction, then reverse the direction for 30 seconds.",
                    "Complete 5 rounds (alternating directions). Keep your back straight and stay low.",
                ],
                "duration": "10 minutes",
                "reps": "5 rounds (30s each direction)",
                "focus": "Coordination, soft hands, and low body control",
            },
            "in_out_crossovers": {
                "label": "In-and-Out Crossovers",
                "instructions": [
                    "Stand in a balanced athletic stance, ball in your right hand.",
                    "Dribble toward the outside (right), fake an in-and-out motion — push the ball out then snap it back.",
                    "Cross the ball over to your left hand and push off your right foot to change direction.",
                    "Mirror the move going left: in-and-out fake, then cross to right hand.",
                    "Each crossover should be sharp and low — keep the ball below your knee.",
                    "Perform 3 sets of 20 crossovers (10 each direction per set).",
                    "Add a step forward on the crossover to simulate attacking a defender.",
                ],
                "duration": "15 minutes",
                "reps": "3 sets of 20 crossovers",
                "focus": "Change of direction, deception, and low controlled dribble",
            },
        },
    },
    "finishing": {
        "label": "Finishing",
        "icon": "🎯",
        "subcategories": {
            "layups": {
                "label": "Layups",
                "instructions": [
                    "Start at the right wing. Dribble toward the basket at game speed.",
                    "Take off from your left foot when going right-handed.",
                    "Drive your right knee up to generate lift.",
                    "Lay the ball softly off the backboard at the top square.",
                    "Land balanced and sprint back to the starting spot.",
                    "Alternate sides: 10 right-hand layups, 10 left-hand layups.",
                    "Last set: add a defensive touch to the drill — have a friend lightly contest or imagine a defender and absorb contact before finishing.",
                ],
                "duration": "20 minutes",
                "reps": "5 sets (10 layups each, alternating sides)",
                "focus": "Footwork, soft touch off the glass, and finishing under pressure",
            },
            "euro_steps": {
                "label": "Euro Steps",
                "instructions": [
                    "Start at the top of the key, drive hard to your right.",
                    "Take a long step to the right with your right foot (first step).",
                    "Immediately plant and take a long lateral step to the left (second step).",
                    "Finish with your left hand or right hand depending on the angle.",
                    "The key is the lateral step — it must be explosive to beat the defender.",
                    "Drill it slow first: walk-through 5 times, then half-speed 5 times, then full speed.",
                    "Complete 4 sets of 10 euro steps, alternating the finishing hand each rep.",
                ],
                "duration": "20 minutes",
                "reps": "4 sets of 10 reps",
                "focus": "Two-step timing, body control, and finishing through contact",
            },
            "floaters": {
                "label": "Floaters",
                "instructions": [
                    "Start at the elbow (free throw line extended). Drive toward the middle of the lane.",
                    "One or two steps into the lane, release the ball with a high, soft arc.",
                    "Use your wrist to guide the ball — imagine lobbing it over a tall defender.",
                    "The release point is higher than a regular layup but before your body fully extends.",
                    "Practice off one foot (running floater) and off two feet (stop-and-pop floater).",
                    "Shoot 10 from the right side, 10 from the left side.",
                    "Complete 4 total sets. On the last set, add a dribble move (crossover or hesitation) before driving.",
                ],
                "duration": "20 minutes",
                "reps": "4 sets of 20 floaters",
                "focus": "High arc, soft touch, and finishing over shot-blockers",
            },
        },
    },
}


@app.route("/")
def index():
    categories = {k: {"label": v["label"], "icon": v["icon"]} for k, v in WORKOUTS.items()}
    return render_template("index.html", categories=categories)


@app.route("/workout/<category>")
def workout(category):
    if category not in WORKOUTS:
        return redirect(url_for("index"))
    cat = WORKOUTS[category]
    sub_key = random.choice(list(cat["subcategories"].keys()))
    sub = cat["subcategories"][sub_key]
    return render_template(
        "workout.html",
        category_label=cat["label"],
        category_key=category,
        workout=sub,
    )


if __name__ == "__main__":
    app.run(debug=True)
