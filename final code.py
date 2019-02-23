#add and sub instructions are right
#input pass test
#rol and ror and translated into 11 byte binary format
#hlt passes test
#no calling of set flags after each operand 
#no calling of assemble operands for some instructions

import sys #for hlt button
import tkinter as tk #for interface creation
import tkinter.filedialog #for file picker button
import copy #to use method to copy dictionaries
import re #to search positio of a lower case letter in a string 

class App(tk.Frame):
    """"application class from wchich main program will be launched"""
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("x86 emulator") #set title
        self.master.tk_setPalette(background='lavender') #set background color

    # drawing the main window and its widgets
        #self.master.overrideredirect(True)
        #self.master.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry("%dx%d+0+0" % (w, h))

        #label
        title_label=tk.Label(master, text="x8086 emulator") #title
        title_label.configure(font=("Helvetica", 12, "bold")) #configure title
       
        #frames
        editor_and_console_frame=tk.Frame(master) #I had to create this frame to position widgets as I intended to

        self.text_frame= tk.LabelFrame(editor_and_console_frame, text="Code editor" ) 
        self.text_frame.configure(font=("Arial", 11))
        manipulation_button_frame = tk.Frame(self.text_frame) #for code manipulation buttons
       
        console_frame=tk.LabelFrame(editor_and_console_frame, text="Console")
        console_frame.configure(font=("Arial", 11))
        speed_button_frame = tk.Frame(console_frame) #for speed control

        diagram_frame=tk.LabelFrame(master, text="Architecture Diagram")
        diagram_frame.configure(font=("Arial", 11))


        #text editor
        self.text_editor = tk.Text(self.text_frame,height=30,width=50, bg='navajo white') 
        DAT_text="MY_DATA SEGEMENT PARA STACK #this is a comment \nVAR DW 0 #this is a user variable \nMY_DATA ENDS \nSTART" #use 0 instead of DUP(?)
        self.text_editor.insert(tk.END, DAT_text) 
        self.text_editor.configure(font=("Courier New", 10)) #set the font style and size in text editor (same as python)
        
        #console
        self.console_window = tk.Text(console_frame, height=20,width=50, state='disabled')

        #buttons
        help=tk.Button(manipulation_button_frame, text='Help', command=self.click_help)
        help.configure(font=("Calibri", 12), relief="groove") #each button has same configuration

        load=tk.Button(manipulation_button_frame, text='Load', command=self.file_picker)
        load.configure(font=("Calibri", 12), relief="groove")

        save=tk.Button(manipulation_button_frame, text='Save', command=self.click_save)
        save.configure(font=("Calibri", 12), relief="groove")

        compile=tk.Button(manipulation_button_frame, text='Compile', command=self.click_compile)
        compile.configure(font=("Calibri", 12), relief="groove")

        clear=tk.Button(manipulation_button_frame, text='Clear', comman=self.click_clear)
        clear.configure(font=("Calibri", 12), relief="groove")

        run=tk.Button(speed_button_frame, text='Run', command=lambda: self.wait_var.set(2))
        run.configure(font=("Calibri", 12), relief="groove")

        halt=tk.Button(speed_button_frame, text='Halt', command=self.click_halt)
        halt.configure(font=("Calibri", 12), relief="groove")

        self.wait_var=tk.IntVar()
        self.step=tk.Button(speed_button_frame, text='Step', command=lambda: self.wait_var.set(1)) # change wait variable to onw
        self.step.configure(font=("Calibri", 12), relief="groove")

        #architecture diagram components: RAM, CPU, buses, I/O boxes and clock cycle counter box
        #RAM
        self.ram_frame=tk.LabelFrame(diagram_frame, text="RAM")
        
        RAM_HEIGHT = 16
        RAM_WIDTH = 8
        counter=0
        for i in range(0,RAM_HEIGHT): #Rows
            for j in range(0,RAM_WIDTH): #Columns
                
                if i%2==0:
                    self.entryfield_name=tk.Label(self.ram_frame, text=str(counter).zfill(2)) 
                    #place labels on even number of rows (row counter starts from 0) 
                    self.entryfield_name.grid(in_=self.ram_frame, row=i, column=j) 
                    self.entryfield_name.configure(font=("Calibri", 12))
                    counter+=1
                else: 
                    self.defaulttext=tk.StringVar() # default value of the field
                    self.entryfield = tk.Entry(self.ram_frame, width=8, borderwidth=5, textvariable=self.defaulttext)
                    self.defaulttext.set("0000") #fill in the box
                    self.entryfield.grid(in_=self.ram_frame, row=i, column=j) #place entry field boxes on odd number of rows
                    self.entryfield.configure(font=("Calibri", 12), justify='center', state='readonly')
                    
        #for entryfield in ram_frame.grid_slaves():
         #   if int(entryfield.grid_info()['row'])%2 != 0:
          #     entryfield.grid_remove()   ####!!!!! instead of going through an new  for loop and deleting the spaces
                
        #place them in functional form
        #opcode=tk.StringVar() # default value of the field
        #opcode_label = tk.Entry(ram_frame, width=6, borderwidth=5, textvariable=defaulttext)
        #defaulttext.set("0000") #fill in the box
        #entryfield.grid(in_=ram_frame, row=i, column=j, ipady=5) #place entry field boxes on odd number of rows
        #entryfield.configure(font=("Calibri", 12), justify='center', state='readonly')
        #CPU components 
        cpu_frame=tk.LabelFrame(diagram_frame, text="CPU")

        #PC
        pc_frame=tk.LabelFrame(cpu_frame)
        pc_label=tk.Label(pc_frame, text="PC")
        pc_label.configure(font=("Calibri", 12))
        self.pc_text=tk.StringVar() # default value of the field       
        self.pc_text.set("00") #fill in the box
        self.pc_box=tk.Entry(pc_frame, width=6, borderwidth=5, textvariable=self.pc_text)
        self.pc_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #MAR
        mar_frame=tk.LabelFrame(cpu_frame)
        mar_label=tk.Label(mar_frame, text="MAR")
        mar_label.configure(font=("Calibri", 12))
        self.mar_text=tk.StringVar() # default value of the field       
        self.mar_text.set("0") #fill in the box
        self.mar_box=tk.Entry(mar_frame, width=6, borderwidth=5, textvariable=self.mar_text)
        self.mar_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #MDR
        mdr_frame=tk.LabelFrame(cpu_frame)
        mdr_label=tk.Label(mdr_frame, text="MDR")
        mdr_label.configure(font=("Calibri", 12))
        self.mdr_text=tk.StringVar() # default value of the field       
        self.mdr_text.set("0") #fill in the box
        self.mdr_box=tk.Entry(mdr_frame, width=6, borderwidth=5, textvariable=self.mdr_text)
        self.mdr_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #ALU contain: registers and flags
        alu_frame=tk.LabelFrame(cpu_frame)

        #registers
        registers_frame=tk.LabelFrame(alu_frame, text="Registers")
        registers_frame.configure(font=("Calibri", 14, 'bold'))

        ax_label=tk.Label(registers_frame, text="AX")
        ax_label.configure(font=("Calibri", 12))
        
        self.ax_text=tk.StringVar() # default value of the field       
        self.ax_text.set("0") #fill in the box
        self.ax_box=tk.Entry(registers_frame, width=6, borderwidth=5, textvariable=self.ax_text)
        self.ax_box.configure(font=("Calibri", 12), justify='center', state='readonly')
        bx_label=tk.Label(registers_frame, text="BX")
        bx_label.configure(font=("Calibri", 12))
        self.bx_text=tk.StringVar() # default value of the field       
        self.bx_text.set("0") #fill in the box
        self.bx_box=tk.Entry(registers_frame, width=6, borderwidth=5, textvariable=self.bx_text)
        self.bx_box.configure(font=("Calibri", 12), justify='center', state='readonly')
        cx_label=tk.Label(registers_frame, text="CX")
        cx_label.configure(font=("Calibri", 12))
        self.cx_text=tk.StringVar() # default value of the field       
        self.cx_text.set("0") #fill in the box
        self.cx_box=tk.Entry(registers_frame, width=6, borderwidth=5, textvariable=self.cx_text)
        self.cx_box.configure(font=("Calibri", 12), justify='center', state='readonly')
        dx_label=tk.Label(registers_frame, text="DX")
        dx_label.configure(font=("Calibri", 12))
        self.dx_text=tk.StringVar() # default value of the field       
        self.dx_text.set("0") #fill in the box
        self.dx_box=tk.Entry(registers_frame, width=6, borderwidth=5, textvariable=self.dx_text)
        self.dx_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #flags and ALU box
        flags_and_ALU_box_frame=tk.Frame(alu_frame)
        ALU_box_frame=tk.LabelFrame(flags_and_ALU_box_frame)
        flags_frame=tk.LabelFrame(flags_and_ALU_box_frame, text="Flags")
        flags_frame.configure(font=("Calibri", 14, 'bold'))

        of_label=tk.Label(flags_frame, text="OF")
        self.of_text=tk.StringVar() # default value of the field       
        self.of_text.set("0") #fill in the box
        self.of_box=tk.Entry(flags_frame, width=6, borderwidth=5, textvariable=self.of_text)
        self.of_box.configure(font=("Calibri", 12), justify='center', state='readonly')
        sf_label=tk.Label(flags_frame, text="SF")
        self.sf_text=tk.StringVar() # default value of the field       
        self.sf_text.set("0") #fill in the box
        self.sf_box=tk.Entry(flags_frame, width=6, borderwidth=5, textvariable=self.sf_text)
        self.sf_box.configure(font=("Calibri", 12), justify='center', state='readonly')
        zf_label=tk.Label(flags_frame, text="ZF")
        self.zf_text=tk.StringVar() # default value of the field       
        self.zf_text.set("0") #fill in the box
        self.zf_box=tk.Entry(flags_frame, width=6, borderwidth=5, textvariable=self.zf_text)
        self.zf_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        self.alu_label=tk.Label(ALU_box_frame, text="ALU")
        self.alu_label.configure(font=("Calibri", 14, 'bold'))
        self.alu_text=tk.StringVar() # default value of the field       
        self.alu_text.set("0") #fill in the box

        #CU contains CIR and dcode table
        cu_frame=tk.LabelFrame(cpu_frame)

        #CU as a separate box
        cu_label_frame=tk.LabelFrame(cu_frame)
        self.cu_label=tk.Label(cu_label_frame, text="CU  ")
        self.cu_label.configure(font=("Calibri", 14, 'bold'))


        #CIR
        cir_frame=tk.LabelFrame(cu_frame)
        cir_label=tk.Label(cir_frame, text="CIR")
        cir_label.configure(font=("Calibri", 12))

        cir_boxes_frame=tk.Frame(cir_frame)
        
        mnemonic_frame=tk.Frame(cir_boxes_frame)
        mnemonic_label=tk.Label(mnemonic_frame, text="opcode")
        self.mnemonic_text=tk.StringVar() # default value of the field       
        self.mnemonic_box=tk.Entry(mnemonic_frame, width=6, borderwidth=5, textvariable=self.mnemonic_text)
        self.mnemonic_text.set("0") #fill in the box
        self.mnemonic_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        operand1_frame=tk.Frame(cir_boxes_frame)
        operand1_label=tk.Label(operand1_frame, text="operand1")
        self.operand1_text=tk.StringVar() # default value of the field       
        self.operand1_box=tk.Entry(operand1_frame, width=6, borderwidth=5, textvariable=self.operand1_text)
        self.operand1_text.set("0") #fill in the box
        self.operand1_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        operand2_frame=tk.Frame(cir_boxes_frame)
        operand2_label=tk.Label(operand2_frame, text="operand2")
        self.operand2_text=tk.StringVar() # default value of the field       
        self.operand2_box=tk.Entry(operand2_frame, width=6, borderwidth=5, textvariable=self.operand2_text)
        self.operand2_text.set("0") #fill in the box
        self.operand2_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #decode unit
        decode_frame=tk.LabelFrame(cu_frame)
        decode_label=tk.Label(decode_frame, text="Decode Unit")
        decode_label.configure(font=("Calibri", 12))
        self.decode_table=tk.Frame(decode_frame)

        #decode table
        instruction_label=tk.Label(self.decode_table, text="Instruction")
        instruction_label.configure(font=("Calibri", 12), relief="groove")
        opcode_label=tk.Label(self.decode_table, text="Opcode")
        opcode_label.configure(font=("Calibri", 12), relief="groove")
        row_counter=1
        for key in decode_dic.keys():
            key_label=tk.Label(self.decode_table, text=key)
            key_label.configure(font=("Calibri", 11), relief="groove")
            key_label.grid(row=row_counter, column=0, sticky="news")
            value_label=tk.Label(self.decode_table, text=decode_dic[key])
            value_label.configure(font=("Calibri", 11), relief="groove")
            value_label.grid(row=row_counter, column=1, sticky="news")
            row_counter+=1
        
        #frame for I/O and 
        input_output_frame=tk.Frame(diagram_frame)

        input_frame=tk.LabelFrame(input_output_frame)

        input_label=tk.Label(input_frame, text="INP")
        input_label.configure(font=("Calibri", 12))
        input_box_text=tk.IntVar()
        self.input_box=tk.Entry(input_frame, width=6, borderwidth=5, textvariable=input_box_text)
        input_box_text.set(0)
        self.input_box.configure(font=("Calibri", 12), justify='center', state='normal', bg='navajo white')

        #submit button
        self.var=tk.IntVar()
        self.submit=tk.Button(input_frame, text='Submit', command=lambda: self.var.set(1))
        self.submit.configure(font=("Calibri", 12), relief="groove")

        output_frame=tk.LabelFrame(input_output_frame)

        output_label=tk.Label(output_frame, text="OUT")
        output_label.configure(font=("Calibri", 12))

        self.output_text=tk.StringVar() # default value of the field       
        output_box=tk.Entry(output_frame, width=6, borderwidth=5, textvariable=self.output_text)
        self.output_text.set("0") #fill in the box
        output_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #clock counter
        cycle_frame=tk.Frame(diagram_frame)

        cycle_label=tk.Label(cycle_frame, text="clock cycle counter")
        cycle_label.configure(font=("Calibri", 12))
        cycle_box=tk.Entry(cycle_frame, width=6, borderwidth=5)
        cycle_box.configure(font=("Calibri", 12), justify='center', state='readonly')

        #packing widgets
        #master frames
        title_label.pack(anchor='n')
        editor_and_console_frame.pack(anchor='n', side='left')
        diagram_frame.pack(anchor='n',side='left', fill='both', expand=True) # fill in the remaining space in the master root

        #editor and console frames 
        self.text_frame.pack(side='top')
        console_frame.pack(anchor='n')

        #button frame code manipulation buttons
        manipulation_button_frame.pack(side='top')
        self.text_editor.pack(side='top')

        load.pack(side='left', padx=5, pady=5)
        save.pack(side='left', padx=5)
        compile.pack(side='left', padx=5)
        clear.pack(side='left', padx=5)
        help.pack(side='left', padx=5)

        #button frame speed buttons
        speed_button_frame.pack(side='top')
        self.console_window.pack(side='top')
        run.pack(side='left', padx=5, pady=5)
        self.step.pack(side='left', padx=5)
        halt.pack(side='left', padx=5)

        #frames in diagram_frames
        self.ram_frame.pack(anchor='n', side='right')
        cpu_frame.pack( side='left', fill='both', expand=1)

        master.update() #GUI needs to be refreshed after cpu_frame is filled in with widgets 
                        #to use new values of diagram_frame.winfo_height() and width() 
                        #otherwise height and width equal to default value one
                        #bus canvas needs to be intialized after other widgets in diagram_frame root widget
        bus_canvas = tk.Canvas(diagram_frame, width=300, height=diagram_frame.winfo_height()) 
        bus_canvas.pack(side='left')
        
        input_output_frame.place(x=700, y=600)
        cycle_frame.place(x=900, y=600)
        
        
        #frames inside cpu frame: pc, mar, alu, mdr, cu 
        #pc
        pc_frame.grid(row=0, column=0)

        #mar
        mar_frame.grid(row=0, column=1)
        
        cpu_frame.columnconfigure(0, weight=1)#configure columns so pc and mar frames 
                                              #occupy same amount of space in their root widget
        cpu_frame.columnconfigure(1, weight=1)

        #alu
        alu_frame.grid(row=1, column=0, sticky="news")

        #mdr
        mdr_frame.grid(row=1, column=1)

        cpu_frame.rowconfigure(0, weight=1)#configure rows so that they occupy same amount of space
                                           #in their root widget
        cpu_frame.rowconfigure(1, weight=1)

        #cu
        cu_frame.grid(row=2, column=0, sticky="news", columnspan=2)
        cpu_frame.rowconfigure(2, weight=2)

        #widgets inside pc_frame
        pc_label.pack()
        self.pc_box.pack()

        #widgets inside mar frame
        mar_label.pack()
        self.mar_box.pack()

        #widgets inside mdr frame
        mdr_label.pack()
        self.mdr_box.pack()

        #widgets inside alu frame: registers, flags and alu frame
        registers_frame.pack(side='top')
        flags_and_ALU_box_frame.pack(side='top')

        #widgets inside flags and alu frame
        flags_frame.pack(side='left')
        ALU_box_frame.pack(side='left', padx=20, pady=20)
        
        #widgets inside registers frame
        ax_label.pack(side='left')
        self.ax_box.pack(side='left')
        bx_label.pack(side='left')
        self.bx_box.pack(side='left')
        cx_label.pack(side='left')
        self.cx_box.pack(side='left')
        dx_label.pack(side='left')
        self.dx_box.pack(side='left')


        #widgets inside flags frame
        of_label.pack(side='left')
        self.of_box.pack(side='left')
        sf_label.pack(side='left')
        self.sf_box.pack(side='left')
        zf_label.pack(side='left')
        self.zf_box.pack(side='left')

        #widgets inside alu frame
        self.alu_label.pack()


        #widgets inside CU frame: cir, decode grid
        decode_frame.pack(side="left")
        cu_label_frame.pack(side="right", anchor='n', pady=200)
        cir_frame.pack(side="right", anchor='s', pady=100)
        

        #cu label
        self.cu_label.pack()
        

        #widgets inside decode frame
        decode_label.pack()
        self.decode_table.pack()
        

        #widgets insdie decode_table
        instruction_label.grid(row=0, column=0, sticky="news")
        opcode_label.grid(row=0, column=1, sticky="news")
        self.decode_table.columnconfigure(0, weight=1)
        self.decode_table.columnconfigure(1, weight=1)

        #widgets insede cir frame
        cir_label.pack(side='top')
        cir_boxes_frame.pack(side='top')

        #widgets inside  cir boxes frame
        mnemonic_frame.pack(side='left')
        operand1_frame.pack(side='left')
        operand2_frame.pack(side='left')

        #widgets inside mnemonic frame
        mnemonic_label.pack(side='top')
        self.mnemonic_box.pack(side='top')

        #widgets inside operand1 frame
        operand1_label.pack(side='top')
        self.operand1_box.pack(side='top')

        #widgets inside operand2 frame
        operand2_label.pack(side='top')
        self.operand2_box.pack(side='top')

        #widgets insdie canvas for buses:
        bus_canvas.create_rectangle(0, 40, 300, 80, fill="light blue")
        addresss_bus_box = bus_canvas.create_text((50, 60), text="Address Bus")
        bus_canvas.create_rectangle(0, 140, 300, 180, fill="dodger blue")
        data_bus_box = bus_canvas.create_text((50, 160), text="Data Bus")
        bus_canvas.create_rectangle(0, 400, 300, 440, fill="light slate blue")
        control_bus_box = bus_canvas.create_text((50, 420), text="Control Bus")

        #add labels on top of buses
        self.address_bus_label = tk.Label(bus_canvas, text='')
        self.address_bus_label.config(font=("Calibri", 12))
        self.address_bus_label.pack()
        bus_canvas.create_window(50, 20, window=self.address_bus_label) 

        self.data_bus_label = tk.Label(bus_canvas, text='')
        self.data_bus_label.config(font=("Calibri", 12))
        self.data_bus_label.pack()
        bus_canvas.create_window(50, 120, window=self.data_bus_label) 

        self.control_bus_label = tk.Label(bus_canvas, text='')
        self.control_bus_label.config(font=("Calibri", 12))
        self.control_bus_label.pack()
        bus_canvas.create_window(50, 380, window=self.control_bus_label) 


        #widgets inside input&output frame
        input_frame.pack(side='left')
        input_label.pack(side='top')
        self.input_box.pack(side='top')
        self.submit.pack(side='top')

        output_frame.pack(side='left')
        output_label.pack(side='top')
        output_box.pack(side='top')
        #widgets inside cycle coutner frame
        cycle_label.pack(side='top')
        cycle_box.pack(side='top')
    #button functions  
    def click_compile(self):
        original=self.text_editor.get("1.0", 'end-1c')
        standardize(original)

    def file_picker(self, event=None):
        try:
            #create filedialog instance and open file in read mode
            file = tk.filedialog.askopenfile(parent=root, mode='r', title='Choose a file')
            #get content from the file
            data = file.read()
            #get rid of added characters at the end of the file
            data=data.rstrip()
            #insert the contents of the file to the end of the text widget
            self.text_editor.insert(tk.END, data) 
            file.close()
        except:
            text="\nfile of this format cannot be loaded into text editor"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled

        
    def click_clear(self):
        #renew all variables and registers
        global registers_dic
        registers_dic =  { x:0 for x in registers_dic}
        global user_vars_dic
        user_vars_dic =  { x:0 for x in user_vars_dic}
        #empty ram representation by derawaing it
        RAM_HEIGHT = 16
        RAM_WIDTH = 8
        counter=0
        for i in range(0,RAM_HEIGHT): #Rows
            for j in range(0,RAM_WIDTH): #Columns
                
                if i%2==0:
                    self.entryfield_name=tk.Label(self.ram_frame, text=str(counter).zfill(2)) 
                    #place labels on even number of rows (row counter starts from 0) 
                    self.entryfield_name.grid(in_=self.ram_frame, row=i, column=j) 
                    self.entryfield_name.configure(font=("Calibri", 12))
                    counter+=1
                else: 
                    self.defaulttext=tk.StringVar() # default value of the field
                    self.entryfield = tk.Entry(self.ram_frame, width=8, borderwidth=5, textvariable=self.defaulttext)
                    self.defaulttext.set("0000") #fill in the box
                    self.entryfield.grid(in_=self.ram_frame, row=i, column=j) #place entry field boxes on odd number of rows
                    self.entryfield.configure(font=("Calibri", 12), justify='center', state='readonly')
        
        #empty console window
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.delete('1.0', tk.END)
        app.console_window.config(state="disabled") #and then change it back to disabled

        print("USER DEFINED VARIABLES:", user_vars_dic)
        print("FLAGS:", flags_dic)
        print("REGISTERS:", registers_dic)


        #clear all boxes in architecture diagra and reste background colors to default
        app.pc_box.config(readonlybackground="SystemButtonFace")
        app.pc_text.set(0)
        app.mar_box.config(readonlybackground="SystemButtonFace")
        app.mar_text.set(0)
        app.mdr_box.config(readonlybackground="SystemButtonFace")
        app.mdr_text.set(0)
        app.operand1_box.config(readonlybackground="SystemButtonFace")
        app.operand1_text.set(0)
        app.operand2_box.config(readonlybackground="SystemButtonFace")
        app.operand2_text.set(0)
        app.mnemonic_box.config(readonlybackground="SystemButtonFace")
        app.mnemonic_text.set(0)

        #clear all registers
        app.ax_box.config(readonlybackground="SystemButtonFace")
        app.ax_text.set(0)
        app.bx_box.config(readonlybackground="SystemButtonFace")
        app.bx_text.set(0)
        app.cx_box.config(readonlybackground="SystemButtonFace")
        app.cx_text.set(0)
        app.dx_box.config(readonlybackground="SystemButtonFace")
        app.dx_text.set(0)

        #clear all flags
        app.of_box.config(readonlybackground="SystemButtonFace")
        app.of_text.set(0)
        app.zf_box.config(readonlybackground="SystemButtonFace")
        app.zf_text.set(0)
        app.sf_box.config(readonlybackground="SystemButtonFace")
        app.sf_text.set(0)
        #set ALU and CU boxes to default
        app.cu_label.config(bg="SystemButtonFace") 
        app.alu_label.config(bg="SystemButtonFace") 
        #set all values in decode table to default color
        for label in app.decode_table.grid_slaves(): #change the color back
            label.config(bg='lavender')


    def click_help(self):
        #create a top up window
        help_frame=tk.Toplevel(app.master)
        help_frame.title("Help menu")
        #draw a fullscreen window
        w, h = help_frame.winfo_screenwidth(), help_frame.winfo_screenheight()
        help_frame.geometry("%dx%d+0+0" % (w, h))
        #instruction and directives
        manual=tk.Message(help_frame, text="How to use: \n1.input into editor (by either pressing load button and choosing an example to load or typing directly into the editor) \n2.click compile button \n3.if there are no errors in the code the program will be assembled into ram and user notified \n4 press press run or compile button to run the program and see animation \n below are tables to explain purpose of each mnemonic and architecture diagram")
        manual.pack()
        #insert tables with explanations
        photo = tk.PhotoImage(file="help table 1.gif")
        Artwork1 = tk.Label(help_frame, image=photo)
        Artwork1.photo = photo
        Artwork1.pack(side='left')
       
        photo = tk.PhotoImage(file="help table 2.gif")
        Artwork2 = tk.Label(help_frame, image=photo)
        Artwork2.photo = photo
        Artwork2.pack(side='left')

        photo = tk.PhotoImage(file="registers table.gif")
        Artwork3 = tk.Label(help_frame, image=photo)
        Artwork3.photo = photo
        Artwork3.pack(side='left')

        #old version of the module
        #canvas = tk.Canvas(help_frame)
        #canvas.pack()
        #img=tkinter.PhotoImage(file="help table 2.gif")
        #canvas.image = img
        #canvas.create_image(500,500,image=img)

    def click_save(self):
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str(app.text_editor.get(1.0, tk.END)) # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close() # `()` was missing.

    def click_halt(self):
        sys.exit()

        
def standardize(input):
        if input=="":
            error_generator(0,"empty")


        #split input from code into list of separate lines
        lines=input.splitlines()
        #remove plane space (blank lines) from the submitted code
        while '' in lines:
            lines.remove('')

        formatted_list=[]

        for line in lines:
            line_num=lines.index(line)#used to retrieve current line

            #remove comments (after # charachter)
            sep= '#'
            line=line.split(sep, 1)[0]
            words=line.split(" ")
            while '' in words:
                words.remove('')

            #validation rules
            #check if indentation is correct


            for word in words:
                if word.startswith("\t"):

                    if word=="\t": #output an error if the word is just a single indent
                        text="\nunexpected indent at line "+str(line_num+1)
                        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                        app.console_window.insert(tk.END, text) 
                        app.console_window.config(state="disabled") #and then change it back to disabled

                    elif words.index(word)==0 and word[0:2]=="\t\t": #ouput an error if the line has multiple indents
                        text="\nunexpected indent at line "+str(line_num+1)
                        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                        app.console_window.insert(tk.END, text) 
                        app.console_window.config(state="disabled") #and then change it back to disabled


                    elif words.index(word)==0 and word[0:1]=="\t": #only correct when indent is used on the first word in the line and if it is a single indent
                        words[words.index(word)]=word.replace("\t","") #delete \t from the word
                        words.insert(0,' ') #add white space before word to show the word is indented in 2D array structure

                    else:
                        text="\nunexpected indent at line "+str(line_num)
                        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                        app.console_window.insert(tk.END, text) 
                        app.console_window.config(state="disabled") #and then change it back to disabled
                #error_generator(line_num, "indent")    
            

            while len(words)<4:
                words.append(' ')
            
            if len(words)>4:
                text="\nunexpected operand at line "+str(line_num+1) 
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled
                #error_generator(line_num, "operand_error")
            formatted_list+=words
        global ROWLENGTH
        ROWLENGTH=4
        global NUMBEROFROWS
        NUMBEROFROWS=len(lines)
        twodarray=[[' ' for row in range(ROWLENGTH)] for column in range(NUMBEROFROWS)]
        counter=0

        global start_row  #pointer to keep track of the row from which the main program starts
        start_row=0

        for i in range(0,NUMBEROFROWS): #Row
            for j in range(0,ROWLENGTH): #Columns
                twodarray[i][j]=formatted_list[counter]
                counter+=1

        #the intialize_user_defined_var function is called 
        #at the end of standardize() function

        global error_flag
        error_flag=False
        pc=start_row

        try:
            if twodarray[0]==['MY_DATA', 'SEGEMENT', 'PARA', 'STACK']: 
                intialize_user_defined_variables(twodarray)
                global user_vars_dic

            initialize_user_defined_labels(twodarray)
            pc=start_row
            #during syntax analysis no input is needed so variable for waiting/interrup is set to 1 

            while pc!=NUMBEROFROWS:
                #includes translate intro RAM and detect any syntax errors
                #initialize error free flag here
                pc, answer=syntax_analysis(twodarray, pc, False)
                pc+=1
            #set all variables and registers to 0 and pc to its starting position
            global registers_dic
            registers_dic =  { x:0 for x in registers_dic}
            intialize_user_defined_variables(twodarray)
            pc=start_row
        except:
            pass
        #start function to wait for run/step button click
        #if error free flage is True
        #assemble into ram()
        if error_flag==False:
            text="\ncode has been successfully compiled"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
            step_or_run(twodarray, pc, start_row)
        else:
            #clear RAM
            RAM_HEIGHT = 16
            RAM_WIDTH = 8
            counter=0
            for i in range(0,RAM_HEIGHT): #Rows
                for j in range(0,RAM_WIDTH): #Columns
                
                    if i%2==0:
                        app.entryfield_name=tk.Label(app.ram_frame, text=str(counter).zfill(2)) 
                        #place labels on even number of rows (row counter starts from 0) 
                        app.entryfield_name.grid(in_=app.ram_frame, row=i, column=j) 
                        app.entryfield_name.configure(font=("Calibri", 12))
                        counter+=1
                    else: 
                        app.defaulttext=tk.StringVar() # default value of the field
                        app.entryfield = tk.Entry(app.ram_frame, width=8, borderwidth=5, textvariable=app.defaulttext)
                        app.defaulttext.set("0000") #fill in the box
                        app.entryfield.grid(in_=app.ram_frame, row=i, column=j) #place entry field boxes on odd number of rows
                        app.entryfield.configure(font=("Calibri", 12), justify='center', state='readonly')

            text="\ncode cannot be compiled"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled



def assemble_to_ram(twodarray, pc, start_row):
    pc=start_row
    while pc!=NUMBEROFROWS:
        line=twodarray[pc]

def step_or_run(twodarray,pc, start_row):
    #wait for button click (either run or step)
    app.step.wait_variable(app.wait_var)
    #retrieve wait_var value as a python object (since it is a tkinter variable class)
    wait_var=app.wait_var.get()
    #if step button is clicked the variable is set to zero
    app.console_window.tag_configure("make_bold", font=("Calibri", 12, 'bold')) #create tags to highligh specific lines of code in text and not all of the text widget
    if wait_var==1:
        while pc!=NUMBEROFROWS:
            text="\nCURRENT LINE:\t"+str(twodarray[pc])
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text, "make_bold") #make the current insruction line bold
            ####at first i tried using 
            #app.console_window.tag_add("make_bold", "end-1c linestart", "end") #but it highlighted all of the text widtet 
            #
            #
            app.console_window.config(state="disabled") #and then change it back to disabled
            app.step.wait_variable(app.wait_var) #interrupt
            
            fetch(pc, twodarray, start_row)
            decode(pc, twodarray, start_row)
            global registers_dic
            pc, answer=execute(pc, twodarray, start_row)
            #includes translate intro RAM and detect any syntax errors
            
            global user_vars_dic
            text="\nUPDATED REGISTERS \t" + str(registers_dic)+"\nUPDATED VARIABLES \t" + str(user_vars_dic)+"\nUPDATED FLAGS \t" + str(flags_dic)
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
            

            pc+=1
            #execute the code with an interrup at the end of while loop to wait for step button click
            app.step.wait_variable(app.wait_var)
    #if run is clicked the variable is set to 2
    else:
        #code is executed without an interrupt
        while pc!=NUMBEROFROWS:
            text="\nCURRENT LINE:\t"+str(twodarray[pc])
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text, "make_bold") 
            #includes translate intro RAM and detect any syntax errors
            pc, answer=syntax_analysis(twodarray, pc, True)
            text="\nUPDATED REGISTERS \t" + str(registers_dic)+"\nUPDATED VARIABLES \t" + str(user_vars_dic)+"\nUPDATED FLAGS \t" + str(flags_dic)
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
            pc+=1

def fetch(pc, twodarray, start_row):
    app.pc_box.config(readonlybackground="MistyRose2")
    address=app.pc_text.get() #copy value from accumulator
    retrieve_direct_address(address)
    #copy contents of MDR to CIR
    #but first the temp needs to be separated into mnemonic oparand1 and operand 2 parts
    address=app.mdr_text.get()
    app.mnemonic_text.set(address[0:2]) #mnemonic is always first 2 digits of the address

    try:
        start = re.search("[a-z]", address[::]).start() #find position of the first lower case letter
        end =len(address)-1-re.search("[a-z]", address[::-1]).start()  #find positoin of the last lowercase letter by searching the reversed string
        if start==end: #if there is only one operand
            app.operand1_text.set(address[start:])
            app.operand2_text.set("")
        else: #if there are 2 operands
            app.operand1_text.set(address[start:end])
            app.operand2_text.set(address[end:])
    except: #if there are no operands
        app.operand1_text.set("")
        app.operand2_text.set("")

    text="\ncontents of MDR "+address+" are copied to CIR"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled
    #change color
    app.mdr_box.config(readonlybackground="MistyRose2")
    app.mnemonic_box.config(readonlybackground="MistyRose2")
    app.operand1_box.config(readonlybackground="MistyRose2")
    app.operand2_box.config(readonlybackground="MistyRose2")

    app.step.wait_variable(app.wait_var) #interrupt
    #change color or mdr, cir and ram boxes back to normal
    app.mdr_box.config(readonlybackground="SystemButtonFace")
    app.operand1_box.config(readonlybackground="SystemButtonFace")
    app.operand2_box.config(readonlybackground="SystemButtonFace")
    app.mnemonic_box.config(readonlybackground="SystemButtonFace")

    app.pc_text.set(str(int(app.pc_text.get())+1).zfill(2)) #increment pc
    text="\nprogram counter is incremented"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled
    #change color
    app.pc_box.config(readonlybackground="MistyRose2")

    

def decode(pc, twodarray, start_row):
    app.step.wait_variable(app.wait_var) #interrupt
    #change color of pc back to normal
    app.pc_box.config(readonlybackground="SystemButtonFace")
    temp=app.mnemonic_text.get() #opcode part of the instruction
    
    for label in app.decode_table.grid_slaves():
        if label.cget('text')==temp:
            label.config(bg='MistyRose2') #highlihgt the opcode column
        elif label.cget('text')==decode_dic_rev[temp]: #i cannot get key by value in dictionary so I created a new dictionary with keys and values reversed
            label.config(bg='MistyRose2')

    text="\nopcode "+temp+" corresponds to "+decode_dic_rev[temp]+" instruction"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    app.step.wait_variable(app.wait_var) #interrupt
    for label in app.decode_table.grid_slaves(): #change the color back
        label.config(bg='lavender')

    

def execute(pc, twodarray, start_row):
    _label=0
    mnemonic=1
    operand1=2
    operand2=3
    if twodarray[pc][mnemonic] in arithmetical_operations or twodarray[pc][mnemonic] in bitwise_operations or twodarray[pc][mnemonic] in logical_operations:
        if twodarray[pc][mnemonic]=="NOT":
            if app.operand1_box.get()[0:1]=="r":
                address=twodarray[pc][operand1]
                app.ax_text.set(registers_dic[address])

                text="\ncontents of register "+address+" are copied to AX register"
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled
            
            elif app.operand1_box.get()[0:1]=="d":
                address=app.operand1_box.get()[1:]
                retrieve_direct_address(address)
                app.step.wait_variable(app.wait_var) #interrupt
                #copy address from mdr to AX register
                app.ax_text.set(app.mdr_text.get())
                text="\nretrieved value from MDR "+app.mdr_text.get()+" is copied to AX register"
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled

            app.step.wait_variable(app.wait_var) #interrupt
            pc, answer=syntax_analysis(twodarray, pc, True) #execute instruction

            app.ax_text.set(answer)
            text="\nALU performs NOT operation on contents of AX"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled

            #store the value in first operand
            try: 
            #need dictionary to tie names of registers with associated text variables in register boxes
                registers_boxes_dic[twodarray[pc][operand1]].set(answer) #if first operand is a register
                text="\nValue from AX "+str(answer)+" is stored in register "+twodarray[pc][operand1]
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled
            except: #otherwise it can only be direct address
                write_into_ram(answer, app.operand1_text.get()[1:])

            #update registers:
            #when i tried referencing flag variable directly  
            #app.zf_text.set(str(sf))
            #it would output wrong not updated results 
            app.zf_text.set(str(flags_dic['zf']))
            app.of_text.set(str(flags_dic['of']))
            app.sf_text.set(str(flags_dic['sf']))
            text="\nflags are updated"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled


            return pc, answer

        else:
            #retrieve first operand
            if app.operand1_box.get()[0:1]=="r":
                address=twodarray[pc][operand1]
                #need another dictionary to link names of registers to
                #actually no i can just copy contents of the variable into the location 
                #copy contents of specified address to AX register
                app.ax_text.set(registers_dic[address])

                text="\ncontentents of register "+address+" are copied to AX register"
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled
            
            elif app.operand1_box.get()[0:1]=="d":
                address=app.operand1_box.get()[1:]
                retrieve_direct_address(address)
                app.step.wait_variable(app.wait_var) #interrupt
                #copy address from mdr to AX register
                app.ax_text.set(app.mdr_text.get())
                text="\nretrieved value from MDR "+app.mdr_text.get()+" is copied to AX register"
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled

            app.step.wait_variable(app.wait_var) #interrupt
            pc, answer=syntax_analysis(twodarray, pc, True)

            #retrieve second operand and perform the instruction
            if app.operand2_box.get()[0:1]=="r":
                address=twodarray[pc][operand2]
                app.ax_text.set(answer)
                text="\nALU performs "+twodarray[pc][mnemonic]+" operation with AX register and "+address+" register"
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled

            elif app.operand2_box.get()[0:1]=="d":
                address=app.operand2_box.get()[1:]
                retrieve_direct_address(address)
                app.ax_text.set(answer)
                text="\nALU performs "+twodarray[pc][mnemonic]+" operation with AX register and retrieved value "+app.mdr_text.get()
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled

            elif app.operand2_box.get()[0:1]=="i":
                address=twodarray[pc][operand2]
                app.ax_text.set(answer)
                text="\nALU performs "+twodarray[pc][mnemonic]+" operation with AX register and immediate address "+address
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled

            app.step.wait_variable(app.wait_var) #interrupt

            #store the value in first operand
            try: 
            #need dictionary to tie names of registers with associated text variables in register boxes
                registers_boxes_dic[twodarray[pc][operand1]].set(answer) #if first operand is a register
                text="\nValue from AX "+str(answer)+" is stored in register "+twodarray[pc][operand1]
                app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
                app.console_window.insert(tk.END, text) 
                app.console_window.config(state="disabled") #and then change it back to disabled
            except: #otherwise it can only be direct address
                write_into_ram(answer, app.operand1_text.get()[1:])

            #update registers:
            #when i tried referencing flag variable directly  
            #app.zf_text.set(str(sf))
            #it would output wrong not updated results 
            app.zf_text.set(str(flags_dic['zf']))
            app.of_text.set(str(flags_dic['of']))
            app.sf_text.set(str(flags_dic['sf']))
            text="\nflags are updated"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
            return pc, answer

    elif twodarray[pc][mnemonic] in jump_operations:
        global jump_flag
        text="\nALU decides whether condition for jump is being met"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled

        app.step.wait_variable(app.wait_var) #interrupt
        pc, answer=syntax_analysis(twodarray, pc, True)

        if jump_flag==True:
            app.pc_text.set(app.operand1_text.get()[1:])
            text="\nCondition for jump has been met, address of memory location where instruction starts is copied to PC"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
        else: #jump has not been made 
            text="\nCondition for jump has not been met, next instruciton is fetched"
            app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
            app.console_window.insert(tk.END, text) 
            app.console_window.config(state="disabled") #and then change it back to disabled
        return pc, answer

    elif twodarray[pc][mnemonic]=="HLT":
        app.control_bus_label.config(text="halt")
        text="\nControl unit sends signals to halt execution of the program"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
        pc, answer=syntax_analysis(twodarray, pc, True) #execute instruction
        return pc, answer

    elif twodarray[pc][mnemonic]=="IN":
        pc, answer=syntax_analysis(twodarray, pc, True) #execute instruction
        app.ax_text.set(answer)
        app.data_bus_label.configure(text=answer)
        text="\nValue from input port is tranfserred to AX through data bus"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
        return pc, answer

    elif twodarray[pc][mnemonic]=="OUT":
        pc, answer=syntax_analysis(twodarray, pc, True) #execute instruction
        app.output_text.set(answer)
        app.data_bus_label.configure(text=answer)
        text="\nValue from AX  is tranfserred to output port through data bus"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
        return pc, answer

def retrieve_direct_address(address):
    app.mar_text.set(address) #paste it into mar
    text="\ndirect address "+address+" is copied to MAR"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(font=("Calibri", 12), state="disabled") #and then change it back to disabled
    #highlight
    app.mar_box.config(readonlybackground="MistyRose2")

    app.step.wait_variable(app.wait_var) #wait for button press (interrupt)
    #change colors of pc box back to original
    app.pc_box.config(readonlybackground="SystemButtonFace")
    address=app.mar_text.get()
    app.address_bus_label.config(text=address)
    text="\naddress "+address+" is sent along the address bus"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    app.step.wait_variable(app.wait_var) #interrupt
    app.control_bus_label.config(text="memory read")
    text="\ncontrol unit sends 'read' signal to memory controller along control bus"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled
    #change color
    app.cu_label.config(bg="MistyRose2") 

    app.step.wait_variable(app.wait_var) #interrupt
    #change color or mar box and cu label back to normal
    app.mar_box.config(readonlybackground="SystemButtonFace") 
    app.cu_label.config(bg="SystemButtonFace") 
    ram_address=ram_dic[int(address)] #get instuction from address specified by mar
    ram_row=ram_address[0] 
    ram_column=ram_address[1]
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            value=label.get() #get content from that entry widget
            label.config(readonlybackground="MistyRose2")

    app.data_bus_label.config(text=value) #copy the content to data bus ...
    app.mdr_text.set(value) #to mdr
    app.mdr_box.config(readonlybackground="MistyRose2") #change color of mdr

    text="\ncontents from direct address "+value+" are sent along the data bus to MDR"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    app.step.wait_variable(app.wait_var) #interrupt
    #change color of the ram grid back to normal
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            label.config(readonlybackground="SystemButtonFace") 
    
def write_into_ram(value, address):
    #copy address from operand1 box to mar
    app.mar_text.set(address)
    text="\nDirect address in which value must be stored "+address+" is copied to MAR"
    app.console_window.config(state="normal")
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled")

    app.step.wait_variable(app.wait_var) #interrupt
    app.address_bus_label.config(text=address)
    text="\naddress "+address+" is sent along the address bus"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    #copy data from accumulatro to mdr
    app.mdr_text.set(value)
    text="\nValue from accumulator "+str(value)+" is copied to MDR"
    app.console_window.config(state="normal")
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled")

    app.step.wait_variable(app.wait_var) #interrupt
    app.data_bus_label.config(text=str(value))
    text="\nvalue "+str(value)+" is sent along the data bus"
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    app.step.wait_variable(app.wait_var) #interrupt
    app.control_bus_label.config(text="memory write")
    text="\ncontrol unit sends 'write' signal to memory controll along control bus to write value "+str(value)+" into memory address "+address
    app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") #and then change it back to disabled

    app.step.wait_variable(app.wait_var) #interrupt
    #write data into specified memory box
    ram_address=ram_dic[int(address)] #get instuction from address specified by mar
    ram_row=ram_address[0] 
    ram_column=ram_address[1]
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            new_text=tk.StringVar() # new value of the field
            label.configure(textvariable=new_text)
            new_text.set(value) #fill in the box 

    text="\nvalue "+str(value)+" is written into address "+address
    app.console_window.config(state="normal")
    app.console_window.insert(tk.END, text) 
    app.console_window.config(state="disabled") 

def intialize_user_defined_variables(twodarray):
    _label=0
    mnemonic=1
    operand1=2
    operand2=3
    row=1
    #counter needed to calculate location of the memory box from the end of RAM to store content of the variable 
    offset=0
    global start_row
    try:
        while twodarray[row]!=['MY_DATA', 'ENDS', ' ', ' ']:
            if twodarray[row][mnemonic]=="DW":
                try:
                #add key and associated value into user_vars dictionary
                    user_vars_dic[twodarray[row][_label]]=int(twodarray[row][operand1]) 
                    position=63-offset
                    #add variable name and its memory address into user_vars_position dictionary
                    user_vars_position_dic[twodarray[row][_label]]=position
                    #get position of memory box in list format [row, column]
                    ram_address=ram_dic[position]
                    #separate the address into row and column variables
                    ram_row=ram_address[0] 
                    ram_column=ram_address[1]
                    ram_value=int(twodarray[row][operand1])
                    for label in app.ram_frame.grid_slaves():
                        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
                            new_text=tk.StringVar() #new value of the text
                            label.configure(textvariable=new_text)
                            new_text.set(ram_value) #fill in the box
                            #increment offset counter for next variable to be stored
                    offset+=1
                except:
                    error_generator(row, "operand_error")
            else:
                error_generator(row, "mnemonic_error")
            row+=1
        start_row=row+1  # this is the row from which the code segment will start
    except:
        error_generator(row, "data_syntax") 
    
    
    

def initialize_user_defined_labels(twodarray):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    
    #if no user vars were intialized
    #start_row=0 otherwise 
    #it is the line number of end of data segment+1
    global start_row
    #to give a sensible name to a variable
    row_for_label=start_row
    #check is the first column of the first line in code segment is a label
    if twodarray[row_for_label][label]==' ':
        error_generator(row_for_label, "label_error")
    #read each line of code segment until Halt instruction 
    while row_for_label!=NUMBEROFROWS:
        #if label field is not empty
        if twodarray[row_for_label][label]!=' ':
            #add label and its associated line number to the dictionary
            labels_dic[twodarray[row_for_label][label]]=row_for_label 
        row_for_label+=1

def syntax_analysis(twodarray, pc, waiting):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    #check mnemonic for each line of code
    if twodarray[pc][mnemonic] in arithmetical_operations:
        #if in twodarray list in position row=pc and column=mnemonic column =="ADD"
        if twodarray[pc][mnemonic]=="ADD":
            answer=_add(twodarray, pc, pc-start_row) #variable used to store result of arithemetical operation and to update flags registers
        elif twodarray[pc][mnemonic]=="SUB":
            answer=_sub(twodarray, pc, pc-start_row)    
        return pc, answer

    elif twodarray[pc][mnemonic] in bitwise_operations:
        if twodarray[pc][mnemonic]=="ROL": 
            answer=_rol(twodarray, pc, pc-start_row)
        elif twodarray[pc][mnemonic]=="ROR":
            answer=_ror(twodarray, pc, pc-start_row) 
        elif twodarray[pc][mnemonic]=="SHL":
            answer=_shl(twodarray, pc, pc-start_row)
        elif twodarray[pc][mnemonic]=="SHR":
            answer=_shr(twodarray, pc, pc-start_row)       
        return pc, answer
            
    elif twodarray[pc][mnemonic] in data_manipulation:
        answer=_mov(twodarray, pc, pc-start_row) 
        return pc, answer
        
    elif twodarray[pc][mnemonic] in logical_operations:
        if twodarray[pc][mnemonic]=="AND":
            answer=_and(twodarray, pc, pc-start_row)
        elif twodarray[pc][mnemonic]=="OR":
            answer=_or(twodarray, pc, pc-start_row)
        elif twodarray[pc][mnemonic]=="XOR":
            answer=_xor(twodarray, pc, pc-start_row)
        elif twodarray[pc][mnemonic]=="NOT":
            answer=_not(twodarray, pc, pc-start_row)
        return pc, answer

    elif twodarray[pc][mnemonic] in control_operations:
        if twodarray[pc][mnemonic]=="HLT":
            pc, answer=_hlt(twodarray, pc, pc-start_row)
            return pc, answer
        elif twodarray[pc][mnemonic]=="IN":
            if waiting==False:
                answer=_inp2(twodarray, pc, pc-start_row)
            else:
                answer=_inp1(twodarray, pc, pc-start_row)
            return pc, answer
        elif twodarray[pc][mnemonic]=="OUT":
            answer=_out(twodarray, pc, pc-start_row)
            return pc, answer

    elif twodarray[pc][mnemonic] in jump_operations: 
        pc, answer=_jump(twodarray, pc, pc-start_row)
        return pc, answer
    else:
        error_generator(pc, "mnemonic_error")
        answer=0
        return pc, answer
            

def _add(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    # check if 1st operand is an accumulator and 2nd operand is a literal
    if twodarray[pc][operand1]=="AX":
        try:
            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]+int(twodarray[pc][operand2])
            answer=registers_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
        except:
            error_generator(pc, "operand_error")
    else:
        # check if 1st operand is a register and 2nd operand is a literal
        try:
            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]+int(twodarray[pc][operand2])
            answer=registers_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
                    
        except:
            try:
            #check if 1st operand is a user defined variable and 2nd operand is a literal
                user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]]+int(twodarray[pc][operand2])
                answer=user_vars_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            except:
                try:
                    #check if both operands are register
                    registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]+registers_dic[twodarray[pc][operand2]]
                    answer=registers_dic[twodarray[pc][operand1]]
                    assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
                except:
                    #check if 1st operand is a register and 2nd operand is a user defined variable
                    try: 
                        registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]+user_vars_dic[twodarray[pc][operand2]]
                        answer=registers_dic[twodarray[pc][operand1]]
                        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")
                    except:
                        #check if 1st operand is a user defined variable and 2nd operand is a register
                        try:
                            user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]]+registers_dic[twodarray[pc][operand2]]
                            answer=user_vars_dic[twodarray[pc][operand1]]
                            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
                        except:
                            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _sub(twodarray, pc, ram_counter):
   #sub is a reserve word
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
        # check if 1st operand is an accumulator and 2nd operand is a literal
    if twodarray[pc][operand1]=="AX":
        try:
            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]+int(twodarray[pc][operand2])
            answer=registers_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
        except:
            error_generator(pc, "operand_error")
    else:
        try:
            # check if 1st operand is a register and 2nd operand is a literal
            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]-int(twodarray[pc][operand2])
            answer=registers_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
                    
        except:
            try:
            #check if 1st operand is a user defined variable and 2nd operand is a literal
                user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]]-int(twodarray[pc][operand2])
                answer=user_vars_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            except:
                try:
                    #check if both operands are register
                    registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]-registers_dic[twodarray[pc][operand2]]
                    answer=registers_dic[twodarray[pc][operand1]]
                    assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
                except:
                    #check if 1st operand is a register and 2nd operand is a user defined variable
                    try: 
                        registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]]-user_vars_dic[twodarray[pc][operand2]]
                        answer=registers_dic[twodarray[pc][operand1]]
                        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")
                    except:
                        #check if 1st operand is a user defined variable and 2nd operand is a register
                        try:
                            user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]]-registers_dic[twodarray[pc][operand2]]
                            answer=user_vars_dic[twodarray[pc][operand1]]
                            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
                        except:
                            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _rol(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    #first operand can only be register or user defined variable 
    #second operand can only be a literal (integer)
    #check if first operand is a register and second operand is an integer
    try:
        #operand 1 is the number to be rotated and operand 2 is the number of shifts
        num=registers_dic[twodarray[pc][operand1]]
        bits=int(twodarray[pc][operand2])
        #convert to binary (11bytes since +-999 denary number falls in this range) 
        num="{0:{fill}11b}".format(num, fill='0')
        #separate part of the string to rotate
        temp=num[0:bits]
        #add it to the end of the number
        num=num+temp
        #delete rotated characters from the beginning of the number
        num=num[bits:]
        #convert back to decimal
        num=int(num,2)
        answer=num
        #update the variables
        registers_dic[twodarray[pc][operand1]]=answer
        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")

    except:
        try:
            #check if first operand is a user defined variable and second operand is an integer
            num=user_vars_dic[twodarray[pc][operand1]]
            bits=int(twodarray[pc][operand2])
            num="{0:{fill}11b}".format(num, fill='0')
            temp=num[0:bits]
            num=num+temp
            num=num[bits:]
            num=int(num,2)
            answer=num
            user_vars_dic[twodarray[pc][operand1]]=answer
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")

        except:
            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _ror(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    #check if first operand is a register and second operand is an integer
    try:
        #operand 1 is the number to be rotated and operand 2 is the number of shifts
        num=registers_dic[twodarray[pc][operand1]]
        bits=int(twodarray[pc][operand2])
        num="{0:{fill}11b}".format(num, fill='0')
        #separate part of the string to rotate
        temp=num[-bits:]
        #add it to the beginning of the number
        num=temp+num
        #delete rotated characters from the end of the number
        num=num[:-bits]
        num=int(num,2)
        answer=num
        registers_dic[twodarray[pc][operand1]]=answer
        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
    except:
        try:
            #check if first operand is a user defined variable and second operand is an integer
            num=user_vars_dic[twodarray[pc][operand1]]
            bits=int(twodarray[pc][operand2])
            num="{0:{fill}11b}".format(num, fill='0')
            #separate part of the string to rotate
            temp=num[-bits:]
            #add it to the beginning of the number
            num=temp+num
            #delete rotated characters from the end of the number
            num=num[:-bits]
            num=int(num,2)
            answer=num
            user_vars_dic[twodarray[pc][operand1]]=answer
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
        except:
            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _shl(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    try:
        # check if 1st operand is a register and 2nd operand is a literal
        registers_dic[twodarray[pc][operand1]]=(registers_dic[twodarray[pc][operand1]] % 0x100000000) << int(twodarray[pc][operand2])
        answer=registers_dic[twodarray[pc][operand1]]
        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
    except:
        try:
        #check if 1st operand is a user defined variable and 2nd operand is a literal
            user_vars_dic[twodarray[pc][operand1]]=(user_vars_dic[twodarray[pc][operand1]] % 0x100000000) << int(twodarray[pc][operand2])
            answer=user_vars_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
        except:
            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _shr(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    try:
        # check if 1st operand is a register and 2nd operand is a literal
        registers_dic[twodarray[pc][operand1]]=(registers_dic[twodarray[pc][operand1]] % 0x100000000) >> int(twodarray[pc][operand2])
        answer=registers_dic[twodarray[pc][operand1]]
        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
    except:
        try:
        #check if 1st operand is a user defined variable and 2nd operand is a literal
            user_vars_dic[twodarray[pc][operand1]]=(user_vars_dic[twodarray[pc][operand1]] % 0x100000000) >> int(twodarray[pc][operand2])
            answer=user_vars_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
        except:
            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _hlt(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    if twodarray[pc][operand1]==' ' and twodarray[pc][operand2]==' ':
    #set counter to last line of the code to exit execution of the program loop
        new_pc=NUMBEROFROWS
    else:
        error_generator(pc, "operand_error")
    assemble_into_ram_0operands(ram_counter, twodarray[pc][mnemonic])
    #if line/s of code were omitted
    if new_pc > pc+1:
        #save old values
        global user_vars_dic
        old_vars=user_vars_dic.copy()
        global registers_dic
        old_registers=registers_dic.copy()
        global flags_dic
        old_flags=flags_dic.copy()
        while pc+1!=new_pc:
            #execute the omitted lines
            syntax_analysis(twodarray,pc+1, False)
            pc+=1
        #restore the old values
        user_vars_dic=old_vars.copy()
        registers_dic=old_registers.copy()
        flags_dic=old_flags.copy()
    return new_pc-1, answer #pc is incremented in while loop inside standardize function

def _inp1(twodarray, pc, ram_counter): #with waiting 
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    #operand 1 can only be an accumulator and secon variable can only be port name (which is 0)
    if twodarray[pc][operand1]=="AX" and int(twodarray[pc][operand2])==0:
        text="\ntype into input box and press submit"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
        app.submit.wait_variable(app.var) #interrupt to wait for submit button press
        registers_dic["AX"]= int(app.input_box.get())
        answer=int(app.input_box.get())
    else:
        error_generator(pc, "operand_error")

    return answer

def _inp2(twodarray, pc, ram_counter): #without interrupt to assemble into ram
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    try:
        if twodarray[pc][operand1]=="AX" and int(twodarray[pc][operand2])==0:
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "p")
        else:
            error_generator(pc, "operand_error")
    except:
        error_generator(pc, "operand_error")
    return answer

def _out(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    if int(twodarray[pc][operand1])==0 and twodarray[pc][operand2]=="AX":
        #try:
        answer=str(registers_dic["AX"])
        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "p")
        #except:
            
    else:
        error_generator(pc, "operand_error")
    return answer

def _mov(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0

    
    if twodarray[pc][operand1] in registers_dic:
        #both are registers
        if twodarray[pc][operand1] in registers_dic and twodarray[pc][operand2] in registers_dic:
            try:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand2]]
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
            except:
                error_generator(pc, "operand_error")

        # check if 1st operand is a register and 2nd operand is a user defined variable
        elif twodarray[pc][operand1] in registers_dic and twodarray[pc][operand2] in user_vars_dic:
            try:
                registers_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand2]]
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")

            except:
                error_generator(pc, "operand_error")
        else:
            try:
                    # check if 1st operand is a register and 2nd operand is a literal
                registers_dic[twodarray[pc][operand1]]=int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
            except:
                pass

    # check if 1st operand is a user defined variable and 2nd operand is a register
    elif twodarray[pc][operand1] in user_vars_dic and twodarray[pc][operand2] in registers_dic:
        try:
            user_vars_dic[twodarray[pc][operand1]]=int(registers_dic[twodarray[pc][operand2]])
            answer=user_vars_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
        except:
            error_generator(pc, "operand_error")
    #check if 1st operand is a user defined variable and 2nd operand is a literal
    elif twodarray[pc][operand1] in user_vars_dic:
        try:
            user_vars_dic[twodarray[pc][operand1]]=int(twodarray[pc][operand2])
            answer=user_vars_dic[twodarray[pc][operand1]]
            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            pass
        except:
            error_generator(pc, "operand_error")
    else:
        error_generator(pc, "operand_error")
    set_flags(answer)
    return answer


def _jump(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    global jump_flag #needed for execute animation
    if twodarray[pc][mnemonic]=="JMP": #unconditional jump
        try:
            assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
            new_pc=labels_dic[twodarray[pc][operand1]]
            jump_flag=True
        except:
            error_generator(pc, "operand_error")
    elif twodarray[pc][mnemonic]=="JZ": #jump if zero
        global flags_dic 
        #need selection statement to check if there is no second operand and operand 1 is in labels dictionary
        if twodarray[pc][operand1] in labels_dic and twodarray[pc][operand2]==' ':
            if flags_dic["zf"]==True:
                try:
                    assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                    new_pc=labels_dic[twodarray[pc][operand1]]
                    jump_flag=True
                except:
                    error_generator(pc, "operand_error")
            else:
                assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                pc+=1
                new_pc=pc
        else:
            error_generator(pc, "operand_error")

    elif twodarray[pc][mnemonic]=="JNZ": #jump if not zero
        if twodarray[pc][operand1] in labels_dic and twodarray[pc][operand2]==' ':
            if flags_dic["zf"]==False:
                try:
                    assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                    new_pc=labels_dic[twodarray[pc][operand1]]
                    jump_flag=True
                except:
                    error_generator(pc, "operand_error")
            else:
                assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                pc+=1
                new_pc=pc
        else:
            error_generator(pc, "operand_error")

    elif twodarray[pc][mnemonic]=="JL": #jump if less than zero
        if twodarray[pc][operand1] in labels_dic and twodarray[pc][operand2]==' ':
            if flags_dic["sf"]==True:
                try:
                    assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                    new_pc=labels_dic[twodarray[pc][operand1]]
                    jump_flag=True
                except:
                    error_generator(pc, "operand_error")
            else:
                assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                pc+=1
                new_pc=pc
        else:
            error_generator(pc, "operand_error")

    elif twodarray[pc][mnemonic]=="JG": #jump if greater than zero
        if twodarray[pc][operand1] in labels_dic and twodarray[pc][operand2]==' ':
            if flags_dic["sf"]==False and flags_dic["zf"]==False:
                try:
                    assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                    new_pc=labels_dic[twodarray[pc][operand1]]
                    jump_flag=True
                except:
                    error_generator(pc, "operand_error")
            else:
                assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                pc+=1
                new_pc=pc
        else:
            error_generator(pc, "operand_error")

    elif twodarray[pc][mnemonic]=="JLE": #jump if less or equal to zero
        if twodarray[pc][operand1] in labels_dic and twodarray[pc][operand2]==' ':

            if flags_dic["zf"]==True or flags_dic["sf"]==True:
                try:
                    assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                    new_pc=labels_dic[twodarray[pc][operand1]]
                    jump_flag=True
                except:
                    error_generator(pc, "operand_error")
            else:
                assemble_into_ram_1operand(pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
                pc+=1
                #if jump has not been made new_pc variable still needs to be created as it is refenrencd in the next if statement
                new_pc=pc
        else:
            error_generator(pc, "operand_error")
    else:
        error_generator(pc, "mnemonic_error")
    
    #if line/s of code were omitted
    if new_pc > pc+1:
        #save old values
        global user_vars_dic
        old_vars=user_vars_dic.copy()
        global registers_dic
        old_registers=registers_dic.copy()
        old_flags=flags_dic.copy()
        while pc+1!=new_pc:
            #execute the omitted lines
            syntax_analysis(twodarray,pc+1, False)
            pc+=1
        #restore the old values
        user_vars_dic=old_vars.copy()
        registers_dic=old_registers.copy()
        flags_dic=old_flags.copy()
    return new_pc-1, answer #pc is incremented in while loop inside standardize function

def _and(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    # check if 1st operand is an accumulator and 2nd operand is a literal
    if twodarray[pc][operand1]=="AX":

        #check if both operands are either 1 or zero
        if (ax!=0 and ax!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
            error_generator(pc, "operand_error")
        else:
            try:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] and int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
            except:
                error_generator(pc, "operand_error")
    else:
        # check if 1st operand is a register and 2nd operand is a literal
        try:
            if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                error_generator(pc, "operand_error")
            else:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] and int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
                    
        except:
            #check if 1st operand is a user defined variable and 2nd operand is a literal
            try:
                if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                    error_generator(pc, "operand_error")
                else:
                    user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] and int(twodarray[pc][operand2])
                    answer=user_vars_dic[twodarray[pc][operand1]]
                    assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            except:
                #check if both operands are register
                try:
                    if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                        error_generator(pc, "operand_error")
                    else:
                        registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] and registers_dic[twodarray[pc][operand2]]
                        answer=registers_dic[twodarray[pc][operand1]]
                        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
                except:
                    #check if 1st operand is a register and 2nd operand is a user defined variable
                    try: 
                        if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (user_vars_dic[twodarray[pc][operand2]]!=0 and user_vars_dic[twodarray[pc][operand2]]!=1):
                            error_generator(pc, "operand_error")
                        else:
                            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] and user_vars_dic[twodarray[pc][operand2]]
                            answer=registers_dic[twodarray[pc][operand1]]
                            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")
                    except:
                        #check if 1st operand is a user defined variable and 2nd operand is a register
                        try:
                            if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                                error_generator(pc, "operand_error")
                            else:
                                user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] and registers_dic[twodarray[pc][operand2]]
                                answer=user_vars_dic[twodarray[pc][operand1]]
                                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
                        except:
                            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _or(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    # check if 1st operand is an accumulator and 2nd operand is a literal
    if twodarray[pc][operand1]=="AX":

        #check if both operands are either 1 or zero
        if (ax!=0 and ax!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
            error_generator(pc, "operand_error")
        else:
            try:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] or int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
            except:
                error_generator(pc, "operand_error")
    else:
        # check if 1st operand is a register and 2nd operand is a literal
        try:
            if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                error_generator(pc, "operand_error")
            else:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] or int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
                    
        except:
            #check if 1st operand is a user defined variable and 2nd operand is a literal
            try:
                if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                    error_generator(pc, "operand_error")
                else:
                    user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] or int(twodarray[pc][operand2])
                    answer=user_vars_dic[twodarray[pc][operand1]]
                    assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            except:
                #check if both operands are register
                try:
                    if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                        error_generator(pc, "operand_error")
                    else:
                        registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] or registers_dic[twodarray[pc][operand2]]
                        answer=registers_dic[twodarray[pc][operand1]]
                        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
                except:
                    #check if 1st operand is a register and 2nd operand is a user defined variable
                    try: 
                        if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (user_vars_dic[twodarray[pc][operand2]]!=0 and user_vars_dic[twodarray[pc][operand2]]!=1):
                            error_generator(pc, "operand_error")
                        else:
                            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] or user_vars_dic[twodarray[pc][operand2]]
                            answer=registers_dic[twodarray[pc][operand1]]
                            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")
                    except:
                        #check if 1st operand is a user defined variable and 2nd operand is a register
                        try:
                            if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                                error_generator(pc, "operand_error")
                            else:
                                user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] or registers_dic[twodarray[pc][operand2]]
                                answer=user_vars_dic[twodarray[pc][operand1]]
                                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
                        except:
                            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _xor(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0
    # check if 1st operand is an accumulator and 2nd operand is a literal
    if twodarray[pc][operand1]=="AX":

        #check if both operands are either 1 or zero
        if (ax!=0 and ax!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
            error_generator(pc, "operand_error")
        else:
            try:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] ^ int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
            except:
                error_generator(pc, "operand_error")
    else:
        # check if 1st operand is a register and 2nd operand is a literal
        try:
            if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                error_generator(pc, "operand_error")
            else:
                registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] ^ int(twodarray[pc][operand2])
                answer=registers_dic[twodarray[pc][operand1]]
                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "i")
                    
        except:
            #check if 1st operand is a user defined variable and 2nd operand is a literal
            try:
                if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (int(twodarray[pc][operand2])!=0 and int(twodarray[pc][operand2])!=1):
                    error_generator(pc, "operand_error")
                else:
                    user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] ^ int(twodarray[pc][operand2])
                    answer=user_vars_dic[twodarray[pc][operand1]]
                    assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "i")
            except:
                #check if both operands are register
                try:
                    if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                        error_generator(pc, "operand_error")
                    else:
                        registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] ^ registers_dic[twodarray[pc][operand2]]
                        answer=registers_dic[twodarray[pc][operand1]]
                        assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "r")
                except:
                    #check if 1st operand is a register and 2nd operand is a user defined variable
                    try: 
                        if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or (user_vars_dic[twodarray[pc][operand2]]!=0 and user_vars_dic[twodarray[pc][operand2]]!=1):
                            error_generator(pc, "operand_error")
                        else:
                            registers_dic[twodarray[pc][operand1]]=registers_dic[twodarray[pc][operand1]] ^ user_vars_dic[twodarray[pc][operand2]]
                            answer=registers_dic[twodarray[pc][operand1]]
                            assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "r", "d")
                    except:
                        #check if 1st operand is a user defined variable and 2nd operand is a register
                        try:
                            if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or (registers_dic[twodarray[pc][operand2]]!=0 and registers_dic[twodarray[pc][operand2]]!=1):
                                error_generator(pc, "operand_error")
                            else:
                                user_vars_dic[twodarray[pc][operand1]]=user_vars_dic[twodarray[pc][operand1]] ^ registers_dic[twodarray[pc][operand2]]
                                answer=user_vars_dic[twodarray[pc][operand1]]
                                assemble_into_ram_2operands(ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], twodarray[pc][operand2], "d", "r")
                        except:
                            error_generator(pc, "operand_error")
    set_flags(answer)
    return answer

def _not(twodarray, pc, ram_counter):
    label=0
    mnemonic=1
    operand1=2
    operand2=3
    answer=0

    #first operand is a register (including accumulator) and second operand is empty space
    try:
        if (registers_dic[twodarray[pc][operand1]]!=0 and registers_dic[twodarray[pc][operand1]]!=1) or twodarray[pc][operand2]!=' ':
            error_generator(pc, "operand_error")
        else:
            registers_dic[twodarray[pc][operand1]]=int(not(registers_dic[twodarray[pc][operand1]])) #translate boolean into integer
            answer=int(registers_dic[twodarray[pc][operand1]])  
            assemble_into_ram_1operand (pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "r")

    except:
        #check if 1st operand is a user defined variable and second operand is empty space
        try:
            if (user_vars_dic[twodarray[pc][operand1]]!=0 and user_vars_dic[twodarray[pc][operand1]]!=1) or twodarray[pc][operand2]!=' ':
                error_generator(pc, "operand_error")
            else:
                user_vars_dic[twodarray[pc][operand1]]=int(not(user_vars_dic[twodarray[pc][operand1]]))
                #translate boolean into integer
                answer=user_vars_dic[twodarray[pc][operand1]]
                assemble_into_ram_1operand (pc, ram_counter, twodarray[pc][mnemonic], twodarray[pc][operand1], "d")
        except:
            error_generator(pc, "operand_error")
    return answer

def set_flags(answer):
    flags_dic["zf"]=False
    flags_dic["sf"]=False
    flags_dic["of"]=False
    if answer==0:
        flags_dic["zf"]=True
    if answer<0:
        flags_dic["sf"]=True
    if answer not in range(-999, 999):
        flags_dic["of"]=True

def highlighter(event):
    '''the highlight function, called when a Key-press event occurs'''
    for k,v in reserve_words.items(): # iterate over dict
        startIndex = '1.0'
        while True:
            startIndex = app.text_editor.search(k, startIndex, tk.END) # search for occurence of k
            if startIndex:
                endIndex = app.text_editor.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
                app.text_editor.tag_add(k, startIndex, endIndex) # add tag to k
                app.text_editor.tag_config(k, foreground=v)      # and color it with v
                startIndex = endIndex # reset startIndex to continue searching
            else:
                break

def assemble_into_ram_0operands(ram_counter, mnemonic):
    ram_address=ram_dic[ram_counter]
    ram_value=decode_dic[mnemonic]
    ram_row=ram_address[0] 
    ram_column=ram_address[1]
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            new_text=tk.StringVar() # new value of the field
            label.configure(textvariable=new_text)
            new_text.set(ram_value) #fill in the box

def assemble_into_ram_1operand(pc, ram_counter, mnemonic, operand1, operand1_addressing_mode):
    ram_address=ram_dic[ram_counter]
    one=""
    if operand1_addressing_mode=="d":
        try:
            one=str(labels_dic[operand1]-start_row) #if it is a label
        except: #otherwise it can only be a user variable
            one=str(user_vars_position_dic[operand1]) 
    else: #otherwise it is a  regsiter address
        one=operand1
    ram_value=decode_dic[mnemonic]+operand1_addressing_mode+one
    ram_row=ram_address[0] 
    ram_column=ram_address[1]
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            new_text=tk.StringVar() # new value of the field
            label.configure(textvariable=new_text)
            new_text.set(ram_value) #fill in the box

def assemble_into_ram_2operands(ram_counter, mnemonic, operand1, operand2, operand1_addressing_mode, operand2_addressing_mode):
    ram_address=ram_dic[ram_counter]
    one=""
    two=""
    #if direct addressing is used, look up the address of the variable in the dictionary
    if operand1_addressing_mode=="d":
        one=str(user_vars_position_dic[operand1])
        two=operand2
    elif operand2_addressing_mode=="d": #only one of the operands can be direct address
        one=operand1
        two=str(user_vars_position_dic[operand2])
    else:
        one=operand1 #register and immediate addresses are unchanged
        two=operand2
    #translate line of code into opcodes and operands (literals/memory addresses/registers)
    ram_value=decode_dic[mnemonic]+operand1_addressing_mode+one+operand2_addressing_mode+two 

    ram_row=ram_address[0] 
    ram_column=ram_address[1]
    for label in app.ram_frame.grid_slaves():
        if int(label.grid_info()["row"]) == ram_row and int(label.grid_info()["column"]) == ram_column:
            new_text=tk.StringVar() # new value of the field
            label.configure(textvariable=new_text)
            new_text.set(ram_value) #fill in the box
            
def error_generator(line, type):
    line=line+1
    global error_flag
    error_flag=True
    if type=="indent":
        text="\nunexpected indent at line "+str(line)
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
    if type=="operand_error":
        text="\nunexpected operand at line "+str(line)
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled
    if type=="input_error":
        text="\ninappropriate input at line "+str(line)
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled

    if type=="mnemonic_error":
        text="\nunexpected mnemonic at line "+str(line)
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled

    if type=="empty":
        text="\nno input has been detected"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled

    if type=="data_syntax":
        text="\nsyntax error in initializing data segment"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled

    if type=="label_error":
        text="\nfirst line of the code segment must start witha a label"
        app.console_window.config(state="normal") #in order to use insert method i need to change state to normal 
        app.console_window.insert(tk.END, text) 
        app.console_window.config(state="disabled") #and then change it back to disabled



#main program 
if __name__ == '__main__':

    #decode dictionary to fill in decode_table
    decode_dic={"ADD": "01", "SUB":"02", "AND": "03", "OR":"04", "NOT":"05", "XOR": "06", "IN":"07", "OUT": "08",
              "HLT":"09", "JMP": "10", "JZ":"11", "JNZ": "12", "JL":"13", "JG": "14", "JLE":"15","ROL": "16", "ROR":"17", 
              "SHL": "18", "SHR":"19","MOV": "20"}

    #reversed decoe_dic
    decode_dic_rev=dict(zip(decode_dic.values(),decode_dic.keys()))

    #initialize dictionary of user defined variables
    user_vars_dic={}
    user_vars_position_dic={}

    #initialize dictionary of labels
    labels_dic={}

    #initialize set of recognizable instructions by typE
    arithmetical_operations=["ADD", "SUB"]
    logical_operations=["AND", "OR", "NOT", "XOR"]
    control_operations=["IN", "OUT", "HLT"]
    jump_operations=["JMP", "JZ", "JNZ", "JL", "JG", "JLE"]
    bitwise_operations=["ROL","ROR","SHL","SHR"]
    data_manipulation=["MOV"]

    #initialize registers 
    ax=0
    bx=0
    cx=0
    dx=0

    #list of registers
    registers=["AX","BX","CX","DX"]

    #dictionary for registers
    registers_dic={'AX':ax, 'BX':bx, 'CX':cx, 'DX':dx}

    reserve_words={"ADD":'green', "SUB":'green', 
                "AND":'green', "OR":'green', "NOT":'green', "XOR":'green', 
                "IN":'green', "OUT":'green', "HLT":'green', 
                "JMP":'green', "JZ":'green', "JNZ":'green', "JL":'green', "JG":'green', "JLE":'green', 
                "ROL":'green',"ROR":'green',"SHL":'green',"SHR":'green', 
                "MOV":'green',
                "AX":'red', "BX":'red', "CX":'red', "DX":'red'}

    #iniialize flags
    zf=False
    sf=False
    of=False
    #initailze as dictionary instead of just variables to avoid using global variables
    flags_dic={'zf':zf, 'sf':sf, 'of':of}

    ram_dic={0: [1,0], 1: [1,1], 2: [1,2], 3: [1,3], 4: [1,4], 5: [1,5], 6: [1,6], 7: [1,7],
             8: [3,0], 9: [3,1], 10: [3,2], 11: [3,3], 12: [3,4], 13: [3,5], 14: [3,6], 15: [3,7],
             16: [5,0], 17: [5,1], 18: [5,2], 19: [5,3], 20: [5,4], 21: [5,5], 22: [5,6], 23: [5,7],
             24: [7,0], 25: [7,1], 26: [7,2], 27: [7,3], 28: [7,4], 29: [7,5], 30: [7,6], 31: [7,7],
             32: [9,0], 33: [9,1], 34: [9,2], 35: [9,3], 36: [9,4], 37: [9,5], 38: [9,6], 39: [9,7],
             40: [11,0], 41: [11,1], 42: [11,2], 43: [11,3], 44: [11,4], 45: [11,5], 46: [11,6], 47: [11,7],
             48: [13,0], 49: [13,1], 50: [13,2], 51: [13,3], 52: [13,4], 53: [13,5], 54: [13,6], 55: [13,7],
             56: [15,0], 57: [15,1], 58: [15,2], 59: [15,3], 60: [15,4], 61: [15,5], 62: [15,6], 63: [15,7]}


    root = tk.Tk()
    app = App(root)
    app.text_editor.bind('<space>', highlighter)
    registers_boxes_dic={"AX":app.ax_text, "BX":app.bx_text,"CX":app.cx_text,"DX":app.dx_text}
    app.mainloop()







