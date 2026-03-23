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
        
        self.all_boxes = deque()
        self.all_labels = deque()
        self.visible_boxes = VGroup()
        self.visible_labels = VGroup()
        
        self.top_box = None
        self.bottom_box = None
        self.full_stack = None
        self._slot_boxes = []   # invisible layout anchors, one per visible slot
        
        self.scene = None
    
    def make_stack(self, initial_count=5):
        """Create the stack. Use initial_count=0 to start empty."""
        
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

        # One invisible anchor per slot — positions are stable regardless of content
        self._slot_boxes = [
            RoundedRectangle(
                width=self.box_width,
                height=self.box_height,
                corner_radius=self.box_corner_radius,
                stroke_opacity=0,
                fill_opacity=0
            )
            for _ in range(self.max_visible)
        ]

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
                Text(".", font_size=self.font_size).move_to(box)
                for box in initial_boxes
            ]
            
            self.all_boxes.extend(initial_boxes)
            self.all_labels.extend(initial_labels)
        
        self.visible_boxes = VGroup(*initial_boxes)
        self.visible_labels = VGroup(*initial_labels)
        
        # Layout: top anchor → slot anchors → bottom anchor
        self.full_stack = VGroup(self.top_box, *self._slot_boxes, self.bottom_box)
        self.full_stack.arrange(DOWN, buff=self.box_buff).move_to(self.stack_center)

        # Snap initial real boxes onto the slot positions
        for i, (box, label) in enumerate(zip(initial_boxes, initial_labels)):
            box.move_to(self._slot_boxes[i])
            label.move_to(box)
        
        return VGroup(self.full_stack, self.visible_labels)
    
    def set_scene(self, scene):
        self.scene = scene

    def _slot_pos(self, i):
        """Scene-space centre of visible slot i (0 = top)."""
        return self._slot_boxes[i].get_center()

    # ------------------------------------------------------------------
    def add_element(self, text):
        if not self.scene:
            raise ValueError("Scene not set. Call set_scene() first.")
        
        new_box = RoundedRectangle(
            width=self.box_width, 
            height=self.box_height, 
            corner_radius=self.box_corner_radius, 
            color=self.add_color, 
            fill_opacity=0.5
        )
        new_box.move_to(self.top_box)
        new_label = Text(text, font_size=self.font_size).move_to(new_box)
        
        self.scene.add(new_box, new_label)
        
        self.all_boxes.appendleft(new_box)
        self.all_labels.appendleft(new_label)
        
        # Element that scrolls off the bottom when stack overflows
        if len(self.all_boxes) > self.max_visible:
            outgoing_box   = self.all_boxes[self.max_visible]
            outgoing_label = self.all_labels[self.max_visible]
        else:
            outgoing_box   = None
            outgoing_label = None
        
        current_visible = len(self.visible_boxes)  # count before insertion

        # New element drops into slot 0
        animations = [
            new_box.animate.move_to(self._slot_pos(0)),
            new_label.animate.move_to(self._slot_pos(0)),
        ]
        
        # Each existing visible element shifts down one slot
        for i in range(min(current_visible, self.max_visible - 1)):
            animations.extend([
                self.visible_boxes[i].animate.move_to(self._slot_pos(i + 1)),
                self.visible_labels[i].animate.move_to(self._slot_pos(i + 1)),
            ])
        
        if outgoing_box:
            animations.extend([
                FadeOut(outgoing_box,   shift=DOWN),
                FadeOut(outgoing_label, shift=DOWN),
            ])
        
        self.scene.play(*animations, run_time=1)
        
        # Reset colour of element that is no longer the top
        if current_visible > 0:
            self.visible_boxes[0].set_color(self.base_color).set_fill(opacity=0.4)
        
        # Remove outgoing element from visible groups
        if outgoing_box and outgoing_box in self.visible_boxes:
            self.visible_boxes.remove(outgoing_box)
            self.visible_labels.remove(outgoing_label)
            self.scene.remove(outgoing_box, outgoing_label)
        
        # Insert new element at the front
        self.visible_boxes.insert(0, new_box)
        self.visible_labels.insert(0, new_label)
        
        # Enforce cap
        while len(self.visible_boxes) > self.max_visible:
            extra_box   = self.visible_boxes[self.max_visible]
            extra_label = self.visible_labels[self.max_visible]
            self.visible_boxes.remove(extra_box)
            self.visible_labels.remove(extra_label)
            self.scene.remove(extra_box, extra_label)

    # ------------------------------------------------------------------
    def pop_element(self):
        if not self.scene:
            raise ValueError("Scene not set. Call set_scene() first.")
        
        if len(self.visible_boxes) == 0:
            return
        
        top_box   = self.visible_boxes[0]
        top_label = self.visible_labels[0]
        
        if len(self.all_boxes) > self.max_visible:
            incoming_box   = self.all_boxes[self.max_visible]
            incoming_label = self.all_labels[self.max_visible]
            incoming_box.set_color(self.base_color).set_fill(opacity=0.4)
        else:
            incoming_box   = None
            incoming_label = None
        
        # Flash top element red before removing
        self.scene.play(
            top_box.animate.set_color(self.pop_color).set_fill(opacity=0.7),
            top_label.animate.set_color(self.pop_color),
            run_time=0.3
        )
        self.scene.wait(0.2)
        
        animations = []
        current_visible = len(self.visible_boxes)  # includes top (about to leave)

        # Shift remaining visible elements up one slot
        for i in range(min(current_visible - 1, self.max_visible - 1)):
            animations.extend([
                self.visible_boxes[i + 1].animate.move_to(self._slot_pos(i)),
                self.visible_labels[i + 1].animate.move_to(self._slot_pos(i)),
            ])
        
        if incoming_box:
            incoming_box.move_to(self.bottom_box)
            incoming_label.move_to(incoming_box)
            self.scene.add(incoming_box, incoming_label)
            animations.extend([
                incoming_box.animate.move_to(self._slot_pos(self.max_visible - 1)),
                incoming_label.animate.move_to(self._slot_pos(self.max_visible - 1)),
            ])
        else:
            if current_visible >= self.max_visible:
                bottom_box   = self.visible_boxes[self.max_visible - 1]
                bottom_label = self.visible_labels[self.max_visible - 1]
                animations.extend([
                    FadeOut(bottom_box,   shift=UP),
                    FadeOut(bottom_label, shift=UP),
                ])
        
        animations.extend([
            FadeOut(top_box,   shift=UP),
            FadeOut(top_label, shift=UP),
        ])
        
        self.scene.play(*animations, run_time=1)
        
        if top_box in self.all_boxes:
            self.all_boxes.remove(top_box)
            self.all_labels.remove(top_label)
        
        if top_box in self.visible_boxes:
            self.visible_boxes.remove(top_box)
            self.visible_labels.remove(top_label)
        self.scene.remove(top_box, top_label)
        
        if incoming_box:
            self.visible_boxes.add(incoming_box)
            self.visible_labels.add(incoming_label)
        
        # Rebuild visible groups from storage
        self.visible_boxes = VGroup(*list(self.all_boxes)[:self.max_visible])
        self.visible_labels = VGroup(*list(self.all_labels)[:self.max_visible])
        
        for i in range(len(self.visible_boxes)):
            self.visible_boxes[i].set_color(self.base_color).set_fill(opacity=0.4)

    # ------------------------------------------------------------------
    def get_visible_count(self):
        return len(self.visible_boxes)
    
    def get_all_count(self):
        return len(self.all_boxes)
    
    def clear(self):
        if self.scene:
            for box, label in zip(self.visible_boxes, self.visible_labels):
                self.scene.remove(box, label)
        self.all_boxes.clear()
        self.all_labels.clear()
        self.visible_boxes  = VGroup()
        self.visible_labels = VGroup()