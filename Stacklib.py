from manim import *
from collections import deque

class ManimStack:
    def __init__(self, 
                 box_width=2.5, 
                 box_height=0.4, 
                 box_corner_radius=0.1,
                 box_buff=0.1,
                 font_size=14,
                 max_visible=5,
                 add_color=GREEN,
                 base_color=BLUE,
                 pop_color=RED,
                 stack_center=ORIGIN):
        
        # Store configuration - EXACTLY from your code
        self.box_width = box_width
        self.box_height = box_height
        self.box_corner_radius = box_corner_radius
        self.box_buff = box_buff
        self.font_size = font_size
        self.max_visible = max_visible
        self.add_color = add_color
        self.base_color = base_color
        self.pop_color = pop_color
        self.stack_center = stack_center
        
        # Storage - EXACTLY from your code
        self.all_boxes = deque()
        self.all_labels = deque()
        self.visible_boxes = VGroup()
        self.visible_labels = VGroup()
        
        # Invisible anchor boxes
        self.top_box = None
        self.bottom_box = None
        self.full_stack = None
        
        # Scene reference
        self.scene = None
    
    def make_stack(self, initial_count=5):
        """Create the stack - EXACT logic from your code"""
        
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
        
        # Create initial visible rectangles
        initial_boxes = []
        initial_labels = []
        
        if initial_count > 0:
            initial_boxes = [
                RoundedRectangle(
                    width=self.box_width, 
                    height=self.box_height, 
                    corner_radius=self.box_corner_radius, 
                    color=self.base_color, 
                    fill_opacity=0.4,
                    stroke_opacity=1
                )
                for _ in range(initial_count)
            ]
            
            initial_labels = [
                Text(f".", font_size=self.font_size).move_to(box)
                for i, box in enumerate(initial_boxes)
            ]
            
            # Add to storage
            self.all_boxes.extend(initial_boxes)
            self.all_labels.extend(initial_labels)
        
        # Create visible groups
        self.visible_boxes = VGroup(*initial_boxes)
        self.visible_labels = VGroup(*initial_labels)
        
        # Position the stack
        self.full_stack = VGroup(self.top_box, *initial_boxes, self.bottom_box)
        self.full_stack.arrange(DOWN, buff=self.box_buff).move_to(self.stack_center)
        
        # Update label positions
        for label, box in zip(self.visible_labels, self.visible_boxes):
            label.move_to(box)
        
        return VGroup(self.full_stack, self.visible_labels)
    
    def set_scene(self, scene):
        """Set the manim scene for animations"""
        self.scene = scene
    
    def add_element(self, text):
        """EXACT logic from your add_element method"""
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
        
        # Determine outgoing element (6th element)
        if len(self.all_boxes) > self.max_visible:
            outgoing_box = self.all_boxes[self.max_visible]
            outgoing_label = self.all_labels[self.max_visible]
        else:
            outgoing_box = None
            outgoing_label = None
        
        # Prepare animations - EXACT from your code
        animations = [
            new_box.animate.move_to(self.visible_boxes[0]),
            new_label.animate.move_to(self.visible_labels[0]),
        ]
        
        # Shift all visible boxes and labels down
        for i in range(self.max_visible - 1):
            animations.extend([
                self.visible_boxes[i].animate.move_to(self.visible_boxes[i+1]),
                self.visible_labels[i].animate.move_to(self.visible_labels[i+1]),
            ])
        
        # Add outgoing animation
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
        
        # Insert new element at beginning
        self.visible_boxes.insert(0, new_box)
        self.visible_labels.insert(0, new_label)
        
        # Enforce max visible limit
        while len(self.visible_boxes) > self.max_visible:
            extra_box = self.visible_boxes[self.max_visible]
            extra_label = self.visible_labels[self.max_visible]
            self.visible_boxes.remove(extra_box)
            self.visible_labels.remove(extra_label)
            self.scene.remove(extra_box, extra_label)
    
    def pop_element(self):
        """EXACT logic from your pop_element method"""
        if not self.scene:
            raise ValueError("Scene not set. Call set_scene() first.")
        
        if len(self.visible_boxes) == 0:
            return
        
        # Store top element
        top_box = self.visible_boxes[0]
        top_label = self.visible_labels[0]
        
        # Check for incoming hidden element
        if len(self.all_boxes) > self.max_visible:
            incoming_box = self.all_boxes[self.max_visible]
            incoming_label = self.all_labels[self.max_visible]
            incoming_box.set_color(self.base_color).set_fill(opacity=0.4)
        else:
            incoming_box = None
            incoming_label = None
        
        # Highlight top element in red
        self.scene.play(
            top_box.animate.set_color(self.pop_color).set_fill(opacity=0.7),
            top_label.animate.set_color(self.pop_color),
            run_time=0.3
        )
        self.scene.wait(0.2)
        
        # Prepare animations
        animations = []
        
        # Shift all visible boxes and labels up
        for i in range(self.max_visible - 1):
            animations.extend([
                self.visible_boxes[i+1].animate.move_to(self.visible_boxes[i]),
                self.visible_labels[i+1].animate.move_to(self.visible_labels[i]),
            ])
        
        # Add incoming animation
        if incoming_box:
            incoming_box.move_to(self.bottom_box)
            incoming_label.move_to(incoming_box)
            self.scene.add(incoming_box, incoming_label)
            
            animations.extend([
                incoming_box.animate.move_to(self.visible_boxes[self.max_visible - 1]),
                incoming_label.animate.move_to(self.visible_labels[self.max_visible - 1]),
            ])
        else:
            # Fade out bottom box
            if len(self.visible_boxes) >= self.max_visible:
                bottom_box = self.visible_boxes[self.max_visible - 1]
                bottom_label = self.visible_labels[self.max_visible - 1]
                animations.extend([
                    FadeOut(bottom_box, shift=UP),
                    FadeOut(bottom_label, shift=UP),
                ])
        
        # Fade out top element
        animations.extend([
            FadeOut(top_box, shift=UP),
            FadeOut(top_label, shift=UP),
        ])
        
        # Play animations
        self.scene.play(*animations, run_time=1)
        
        # Remove top element from storage
        if top_box in self.all_boxes:
            self.all_boxes.remove(top_box)
            self.all_labels.remove(top_label)
        
        # Remove top element from visible groups
        if top_box in self.visible_boxes:
            self.visible_boxes.remove(top_box)
            self.visible_labels.remove(top_label)
        self.scene.remove(top_box, top_label)
        
        # Update visible groups with incoming element
        if incoming_box:
            self.visible_boxes.add(incoming_box)
            self.visible_labels.add(incoming_label)
        
        # Rebuild visible groups
        self.visible_boxes = VGroup(*list(self.all_boxes)[:self.max_visible])
        self.visible_labels = VGroup(*list(self.all_labels)[:self.max_visible])
        
        # Reset colors
        for i in range(len(self.visible_boxes)):
            self.visible_boxes[i].set_color(self.base_color).set_fill(opacity=0.4)
    
    def get_visible_count(self):
        """Return number of visible elements"""
        return len(self.visible_boxes)
    
    def get_all_count(self):
        """Return total number of elements in storage"""
        return len(self.all_boxes)
    
    def clear(self):
        """Clear all elements"""
        if self.scene:
            for box, label in zip(self.visible_boxes, self.visible_labels):
                self.scene.remove(box, label)
        
        self.all_boxes.clear()
        self.all_labels.clear()
        self.visible_boxes = VGroup()
        self.visible_labels = VGroup()
