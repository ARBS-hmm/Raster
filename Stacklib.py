from manim import *
from collections import deque

class AnimatedStack:
    def __init__(self, 
                 box_width=2.5, 
                 box_height=0.4, 
                 box_corner_radius=0.1,
                 box_buff=0.1,
                 font_size=14,
                 max_visible=5,
                 add_color=GREEN,
                 base_color=BLUE,
                 pop_color=RED):
        
        # Store configuration
        self.box_width = box_width
        self.box_height = box_height
        self.box_corner_radius = box_corner_radius
        self.box_buff = box_buff
        self.font_size = font_size
        self.max_visible = max_visible
        self.add_color = add_color
        self.base_color = base_color
        self.pop_color = pop_color
        
        # Storage
        self.all_boxes = deque()
        self.all_labels = deque()
        self.visible_boxes = VGroup()
        self.visible_labels = VGroup()
        
        # Invisible anchor boxes
        self.top_box = None
        self.bottom_box = None
        self.full_stack = None
        
        # Scene reference (will be set when added to scene)
        self.scene = None
    
    def create_stack(self, center=ORIGIN, initial_count=0):
        """Create the stack VGroup and return it"""
        
        # Create invisible top and bottom boxes
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
        
        # Create initial boxes if needed
        initial_boxes = []
        initial_labels = []
        
        if initial_count > 0:
            initial_boxes = [
                RoundedRectangle(
                    width=self.box_width, 
                    height=self.box_height, 
                    corner_radius=self.box_corner_radius, 
                    color=self.base_color, 
                    fill_opacity=0.4
                )
                for _ in range(initial_count)
            ]
            
            initial_labels = [
                Text(f"Item {i+1}", font_size=self.font_size).move_to(box)
                for i, box in enumerate(initial_boxes)
            ]
            
            self.all_boxes.extend(initial_boxes)
            self.all_labels.extend(initial_labels)
            self.visible_boxes = VGroup(*initial_boxes)
            self.visible_labels = VGroup(*initial_labels)
        
        # Create full stack VGroup
        self.full_stack = VGroup(self.top_box, *initial_boxes, self.bottom_box)
        self.full_stack.arrange(DOWN, buff=self.box_buff).move_to(center)
        
        # Position labels
        for label, box in zip(self.visible_labels, self.visible_boxes):
            label.move_to(box)
        
        return VGroup(self.full_stack, self.visible_labels)
    
    def set_scene(self, scene):
        """Set the manim scene for animations"""
        self.scene = scene
    
    def add_element(self, text):
        """Add an element to the top of the stack"""
        if not self.scene:
            raise ValueError("Scene not set. Call set_scene() first.")
        
        # Create new element
        new_box = RoundedRectangle(
            width=self.box_width, 
            height=self.box_height, 
            corner_radius=self.box_corner_radius, 
            color=self.add_color, 
            fill_opacity=0.5
        )
        new_box.move_to(self.top_box)
        new_label = Text(text, font_size=self.font_size).move_to(new_box)
        
        # Add to scene
        self.scene.add(new_box, new_label)
        
        # Add to storage
        self.all_boxes.appendleft(new_box)
        self.all_labels.appendleft(new_label)
        
        # Determine outgoing element
        outgoing_box = self.all_boxes[self.max_visible] if len(self.all_boxes) > self.max_visible else None
        outgoing_label = self.all_labels[self.max_visible] if len(self.all_labels) > self.max_visible else None
        
        # Prepare animations
        animations = []
        
        if len(self.visible_boxes) > 0:
            animations.extend([
                new_box.animate.move_to(self.visible_boxes[0]),
                new_label.animate.move_to(self.visible_labels[0]),
            ])
        else:
            animations.extend([
                new_box.animate.move_to(self.top_box),
                new_label.animate.move_to(self.top_box),
            ])
        
        # Shift existing boxes down
        for i in range(len(self.visible_boxes) - 1):
            animations.extend([
                self.visible_boxes[i].animate.move_to(self.visible_boxes[i+1]),
                self.visible_labels[i].animate.move_to(self.visible_labels[i+1]),
            ])
        
        # Handle outgoing element
        if outgoing_box:
            animations.extend([
                FadeOut(outgoing_box, shift=DOWN),
                FadeOut(outgoing_label, shift=DOWN),
            ])
        
        # Play animations
        self.scene.play(*animations, run_time=1)
        
        # Reset previous top box color
        if len(self.visible_boxes) > 0:
            self.visible_boxes[0].set_color(self.base_color).set_fill(opacity=0.4)
        
        # Update visible groups
        if outgoing_box and outgoing_box in self.visible_boxes:
            self.visible_boxes.remove(outgoing_box)
            self.visible_labels.remove(outgoing_label)
            self.scene.remove(outgoing_box, outgoing_label)
        
        self.visible_boxes.insert(0, new_box)
        self.visible_labels.insert(0, new_label)
        
        # Enforce max visible limit
        while len(self.visible_boxes) > self.max_visible:
            extra_box = self.visible_boxes[self.max_visible]
            extra_label = self.visible_labels[self.max_visible]
            self.visible_boxes.remove(extra_box)
            self.visible_labels.remove(extra_label)
            self.scene.remove(extra_box, extra_label)
        
        return new_box, new_label
    
    def pop_element(self):
        """Remove an element from the top of the stack"""
        if not self.scene:
            raise ValueError("Scene not set. Call set_scene() first.")
        
        if len(self.visible_boxes) == 0:
            return None, None
        
        # Store top element
        top_box = self.visible_boxes[0]
        top_label = self.visible_labels[0]
        
        # Check for incoming hidden element
        incoming_box = self.all_boxes[self.max_visible] if len(self.all_boxes) > self.max_visible else None
        incoming_label = self.all_labels[self.max_visible] if len(self.all_labels) > self.max_visible else None
        
        if incoming_box:
            incoming_box.set_color(self.base_color).set_fill(opacity=0.4)
        
        # Highlight top element
        self.scene.play(
            top_box.animate.set_color(self.pop_color).set_fill(opacity=0.7),
            top_label.animate.set_color(self.pop_color),
            run_time=0.3
        )
        self.scene.wait(0.2)
        
        # Prepare animations
        animations = []
        
        # Shift remaining boxes up
        for i in range(len(self.visible_boxes) - 1):
            animations.extend([
                self.visible_boxes[i+1].animate.move_to(self.visible_boxes[i]),
                self.visible_labels[i+1].animate.move_to(self.visible_labels[i]),
            ])
        
        # Handle incoming element
        if incoming_box:
            incoming_box.move_to(self.bottom_box)
            incoming_label.move_to(incoming_box)
            self.scene.add(incoming_box, incoming_label)
            
            target_pos = len(self.visible_boxes) - 1
            if target_pos >= 0 and target_pos < len(self.visible_boxes):
                animations.extend([
                    incoming_box.animate.move_to(self.visible_boxes[target_pos]),
                    incoming_label.animate.move_to(self.visible_labels[target_pos]),
                ])
        else:
            # Fade out bottom box if no incoming element
            if len(self.visible_boxes) >= self.max_visible:
                animations.extend([
                    FadeOut(self.visible_boxes[self.max_visible-1], shift=UP),
                    FadeOut(self.visible_labels[self.max_visible-1], shift=UP),
                ])
        
        # Fade out top element
        animations.extend([
            FadeOut(top_box, shift=UP),
            FadeOut(top_label, shift=UP),
        ])
        
        # Play animations
        self.scene.play(*animations, run_time=1)
        
        # Remove top element
        if top_box in self.all_boxes:
            self.all_boxes.remove(top_box)
            self.all_labels.remove(top_label)
        
        if top_box in self.visible_boxes:
            self.visible_boxes.remove(top_box)
            self.visible_labels.remove(top_label)
        self.scene.remove(top_box, top_label)
        
        # Add incoming element
        if incoming_box:
            self.visible_boxes.add(incoming_box)
            self.visible_labels.add(incoming_label)
        
        # Rebuild visible groups
        self.visible_boxes = VGroup(*list(self.all_boxes)[:self.max_visible])
        self.visible_labels = VGroup(*list(self.all_labels)[:self.max_visible])
        
        # Reset colors
        for box in self.visible_boxes:
            box.set_color(self.base_color).set_fill(opacity=0.4)
        
        return top_box, top_label
    
    def get_stack_state(self):
        """Return current stack as list of (box, label) tuples"""
        return list(zip(self.visible_boxes, self.visible_labels))
    
    def clear(self):
        """Remove all elements from the stack"""
        if self.scene:
            for box, label in zip(self.visible_boxes, self.visible_labels):
                self.scene.remove(box, label)
        
        self.all_boxes.clear()
        self.all_labels.clear()
        self.visible_boxes = VGroup()
        self.visible_labels = VGroup()
