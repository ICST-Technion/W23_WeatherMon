from m5stack import *
from m5stack_ui import *
from uiflow import *
import lvgl as lv

LV_HOR_RES=320
LV_VER_RES=240

# A button which gets while holding a press and gets to normal size upon release
class FadingBtn(lv.btn):
  def _event_handler(self, source, evt):
    if evt == lv.EVENT.PRESSING:
        super().set_pos(10, 70)
        super().set_size(300, 100)
        self.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT,lv.font_montserrat_34)

    elif evt == lv.EVENT.RELEASED:
        super().set_pos(self.primal_x, self.primal_y)
        super().set_size(self.primal_w, self.primal_h)
        self.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT,lv.font_montserrat_14)
    
    
  def __init__(self, text, x=0, y=0, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, b_c=0x000000, rad = 1, parent = lv.scr_act()):
    super().__init__(parent, None)
    self.primal_x = x
    self.primal_y = y
    self.primal_w = w
    self.primal_h = h
    btn_label=lv.label(self ,None)
    btn_label.set_text(text)
    self.set_pos(x,y)
    self.set_size(w,h)
    self.set_checkable(False)
    btn_style = lv.style_t()
    btn_style.init()
    btn_style.set_border_color(lv.STATE.DEFAULT, lv.color_hex(b_c))
    btn_style.set_border_width(lv.STATE.DEFAULT, 1)
    btn_style.set_radius(lv.STATE.DEFAULT, 10)
    btn_style.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(bg_c))
    btn_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_c))
    self.add_style(self.PART.MAIN, btn_style)
    self.set_event_cb(self._event_handler)
    
  def set_pos(self, x,y):
    super().set_pos(x,y)
    self.primal_x = x
    self.primal_y = y
  
  def set_x(self, x):
    super().set_x(x)
    self.primal_x = x
    
  def set_y(self, y):
    super().set_y(y)
    self.primal_y = y
    
  def set_size(self, w,h):
    super().set_size(w,h)
    self.primal_w = w
    self.primal_h = h
  
  def set_width(self, w):
    super().set_width(w)
    self.primal_w = w
    
  def set_height(self, h):
    super().set_height(h)
    self.primal_h = h
      
    
class Title():
    def __init__(self, text = '', text_c = 0xFFFFFF, bg_c=0x000000):
        self.text_c = text_c
        self.line = M5Line(x1=0, y1=12, x2=320, y2=12, color=bg_c, width=26, parent=None)
        self.left_label = M5Label(text, x=6, y=5, color=text_c, font=FONT_MONT_14, parent=None)
        self.battery_label = None
        self.icon1 = None
        self.icon2 = None
        
    def clear_title(self):
        if self.icon1:
            self.icon1.delete()
            self.icon1 = None
        if self.icon2:
            self.icon2.delete()
            self.icon2 = None
        if self.battery_label:
            self.battery_label.delete()
            self.battery_label = None
    
    def delete(self):
        if self.icon1: 
            self.icon1.delete()
        if self.icon2:
            self.icon2.delete()
        if self.battery_label:
            self.battery_label.delete()
        if self.line:
            self.line.delete()
        if self.left_label:
            self.left_label.delete()
        
    def set_text(self, text):
        self.left_label.set_text(text)
        
    def show_battery(self):
        per = int((power.getBatVoltage() - 3.2)*100)
        if 80 <= per <= 100:
            bat_sym = lv.SYMBOL.BATTERY_FULL
        elif 50 <= per < 80:
            bat_sym = lv.SYMBOL.BATTERY_3
        elif 20 <= per < 50:
            bat_sym = lv.SYMBOL.BATTERY_2
        elif 5 <= per < 20:
            bat_sym = lv.SYMBOL.BATTERY_1
        else:
            bat_sym = lv.SYMBOL.BATTERY_EMPTY
            
        per_str = str(per) + str('% ') + bat_sym
        self.battery_label = M5Label(per_str, x=265, y=5, color=self.text_c, font=FONT_MONT_14, parent=None)
        
    def remove_battery(self):
        self.battery_label.delete()
        self.battery_label = None
        
    def show_green_wifi(self):
        if self.icon1 is None:
            self.icon1 = M5Img("img/wifi_green.png", x=255, y=0, parent=None)
        else:
            self.icon1.set_img_src("img/wifi_green.png")
            
    def show_red_wifi(self):
        if self.icon1 is None:
            self.icon1 = M5Img("img/wifi_red.png", x=255, y=0, parent=None)
        else:
            self.icon1.set_img_src("img/wifi_red.png")
            
    def remove_wifi(self):
        self.icon1.delete()
        self.icon1 = None

    def show_green_cloud(self):
        if self.icon2 is None:
            self.icon2 = M5Img("img/cloud_green.png", x=225, y=0, parent=None)
        else:
            self.icon2.set_img_src("img/cloud_green.png")
            
    def show_red_cloud(self):
        if self.icon2 is None:
            self.icon2 = M5Img("img/cloud_red.png", x=225, y=0, parent=None)
        else:
            self.icon2.set_img_src("img/cloud_red.png")
            
    def remove_cloud(self):
        self.icon2.delete()
        self.icon2 = None
        






