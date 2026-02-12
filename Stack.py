from manim import *
from collections import deque

class StackedRectangles(Scene):
    def construct(self):
        # Set global attributes for stack appearance
        self.box_width = 2.5
        self.box_height = 0.4
        self.box_corner_radius = 0.1
        self.box_buff = 0.1
        self.font_size = 14
        self.stack_center = LEFT*5+DOWN*3
        
        # Make the stack
        self.make_stack()
        
        # Add elements
        self.add_element("New 1")
        self.add_element("New 2")
        self.add_element("New 3")
        self.add_element("New 4")
        self.add_element("New 5")
        self.add_element("New 6")
        
        # Pop elements
        self.pop_element()
        self.pop_element()
        self.pop_element()
        self.pop_element()
        self.wait()
    
    def make_stack(self, initial_count=5):
        # Store all boxes and labels in deques
        self.all_boxes = deque()
        self.all_labels = deque()
        
        # Create invisible top and bottom boxes using global dimensions
        self.top_box = RoundedRectangle(
            width=self.box_width, 
            height=self.box_height, 
            corner_radius=self.box_corner_radius, 
            stroke_opacity=0, 
            fill_opacity=0
        )
        self.bottom_box = RoundedRectangle(
            width=self.box_width, 
            height=self.box_height, 
            corner_radius=self.box_corner_radius, 
            stroke_opacity=0, 
            fill_opacity=0
        )
        
        # Create initial visible rectangles - ALL INVISIBLE
        initial_boxes = []
        initial_labels = []
        
        if initial_count > 0:
            initial_boxes = [
                RoundedRectangle(
                    width=self.box_width, 
                    height=self.box_height, 
                    corner_radius=self.box_corner_radius, 
                    color=BLUE, 
                    fill_opacity=0,
                    stroke_opacity=0
                )
                for _ in range(initial_count)
            ]
            
            initial_labels = [
                Text(f".", font_size=self.font_size, opacity=0).move_to(box)
                for i, box in enumerate(initial_boxes)
            ]
            
            # Add to our storage
            self.all_boxes.extend(initial_boxes)
            self.all_labels.extend(initial_labels)
        
        # Create visible group (empty if initial_count=0)
        self.visible_boxes = VGroup(*initial_boxes)
        self.visible_labels = VGroup(*initial_labels)
        
        # Position the stack using global center
        self.full_stack = VGroup(self.top_box, *initial_boxes, self.bottom_box)
        self.full_stack.arrange(DOWN, buff=self.box_buff).move_to(self.stack_center)
        
        # Update label positions
        for label, box in zip(self.visible_labels, self.visible_boxes):
            label.move_to(box)
        
        self.add(self.full_stack, self.visible_labels)
        self.wait(0.5)
    
    def add_element(self, text):
        # Create new element using global dimensions
        new_box = RoundedRectangle(
            width=self.box_width, 
            height=self.box_height, 
            corner_radius=self.box_corner_radius, 
            color=GREEN, 
            fill_opacity=0.5
        )
        new_box.move_to(self.top_box)
        new_label = Text(text, font_size=self.font_size).move_to(new_box)
        
        # Add to scene
        self.add(new_box, new_label)
        
        # Add to our full storage
        self.all_boxes.appendleft(new_box)
        self.all_labels.appendleft(new_label)
        
        # Determine which element will be removed from view (the 6th element)
        if len(self.all_boxes) > 5:
            outgoing_box = self.all_boxes[5]
            outgoing_label = self.all_labels[5]
        else:
            outgoing_box = None
            outgoing_label = None
        
        # Prepare animations
        animations = [
            new_box.animate.move_to(self.visible_boxes[0]),
            new_label.animate.move_to(self.visible_labels[0]),
        ]
        
        # Shift all visible boxes and labels down
        for i in range(4):
            animations.extend([
                self.visible_boxes[i].animate.move_to(self.visible_boxes[i+1]),
                self.visible_labels[i].animate.move_to(self.visible_labels[i+1]),
            ])
        
        # Add outgoing animation if we have more than 5 elements
        if outgoing_box:
            animations.extend([
                FadeOut(outgoing_box, shift=DOWN),
                FadeOut(outgoing_label, shift=DOWN),
            ])
        
        # Play all animations
        self.play(*animations, run_time=1)
        
        # Reset the color of the previous top box to blue
        if len(self.visible_boxes) > 0:
            self.visible_boxes[0].set_color(BLUE).set_fill(opacity=0.4)
        
        # Update visible groups
        # Remove outgoing element if it exists
        if outgoing_box and outgoing_box in self.visible_boxes:
            self.visible_boxes.remove(outgoing_box)
            self.visible_labels.remove(outgoing_label)
            self.remove(outgoing_box, outgoing_label)
        
        # Insert new element at the beginning
        self.visible_boxes.insert(0, new_box)
        self.visible_labels.insert(0, new_label)
        
        # Ensure we only have 5 visible elements
        while len(self.visible_boxes) > 5:
            extra_box = self.visible_boxes[5]
            extra_label = self.visible_labels[5]
            self.visible_boxes.remove(extra_box)
            self.visible_labels.remove(extra_label)
            self.remove(extra_box, extra_label)
    
    def pop_element(self):
        # Only pop if there are visible elements
        if len(self.visible_boxes) == 0:
            return
        
        # Store the top element that will be removed
        top_box = self.visible_boxes[0]
        top_label = self.visible_labels[0]
        
        # Store the bottom element that will become visible if we have more in storage
        if len(self.all_boxes) > 5:
            incoming_box = self.all_boxes[5]
            incoming_label = self.all_labels[5]
            incoming_box.set_color(BLUE).set_fill(opacity=0.4)
        else:
            incoming_box = None
            incoming_label = None
        
        # Highlight the top element in red before popping
        self.play(
            top_box.animate.set_color(RED).set_fill(opacity=0.7),
            top_label.animate.set_color(RED),
            run_time=0.3
        )
        self.wait(0.2)
        
        # Prepare animations
        animations = []
        
        # Shift all visible boxes and labels up
        for i in range(4):
            animations.extend([
                self.visible_boxes[i+1].animate.move_to(self.visible_boxes[i]),
                self.visible_labels[i+1].animate.move_to(self.visible_labels[i]),
            ])
        
        # Add incoming animation if we have a hidden element
        if incoming_box:
            # Position the incoming box at the bottom position first
            incoming_box.move_to(self.bottom_box)
            incoming_label.move_to(incoming_box)
            self.add(incoming_box, incoming_label)
            
            animations.extend([
                incoming_box.animate.move_to(self.visible_boxes[4]),
                incoming_label.animate.move_to(self.visible_labels[4]),
            ])
        else:
            # If no incoming element, just fade out the bottom box and label
            bottom_box = self.visible_boxes[4]
            bottom_label = self.visible_labels[4]
            animations.extend([
                FadeOut(bottom_box, shift=UP),
                FadeOut(bottom_label, shift=UP),
            ])
        
        # Fade out the top element (now red)
        animations.extend([
            FadeOut(top_box, shift=UP),
            FadeOut(top_label, shift=UP),
        ])
        
        # Play all animations
        self.play(*animations, run_time=1)
        
        # Remove top element from storage
        if top_box in self.all_boxes:
            self.all_boxes.remove(top_box)
            self.all_labels.remove(top_label)
        
        # Remove top element from visible groups
        if top_box in self.visible_boxes:
            self.visible_boxes.remove(top_box)
            self.visible_labels.remove(top_label)
        self.remove(top_box, top_label)
        
        # Update visible groups with incoming element
        if incoming_box:
            self.visible_boxes.add(incoming_box)
            self.visible_labels.add(incoming_label)
        
        # Ensure we maintain order (visible_boxes should match all_boxes[:5])
        self.visible_boxes = VGroup(*list(self.all_boxes)[:5])
        self.visible_labels = VGroup(*list(self.all_labels)[:5])
        
        # Reset colors - all boxes blue
        for i in range(len(self.visible_boxes)):
            self.visible_boxes[i].set_color(BLUE).set_fill(opacity=0.4)
