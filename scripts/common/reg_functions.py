def parse_instruction(instruction_line, all_instrs):
    # Index 0 = Instruction
    insn_name = instruction_line[0]
    # print(instruction_line)
    # print(insn_name)
    if insn_name in all_instrs:
        insn_subdict = all_instrs[insn_name]
        # print(insn_subdict)
        
        rs1 = rs2 = rd = None
        # Determine type and return accordingly
        if insn_subdict["Format"] == "R":
            # rd, rs1, rs2
            rd = instruction_line[1][:-1]
            rs1 = instruction_line[2][:-1]
            rs2 = instruction_line[3]
        elif insn_subdict["Format"] == "I":
            if (insn_subdict["Type"] == "load"):
                # rd, imm(rs)
                remaining_string = instruction_line[2].replace("(", " ", 1)[:-1].split()
                rs1, rd = remaining_string[1], instruction_line[1][:-1]
            else:
                # rd, rs, imm
                rd, rs1 = instruction_line[1][:-1], instruction_line[2][:-1]
            # TODO : Case for Synch, System and Counters instructions

        elif insn_subdict["Format"] == "S":
            # rs1, imm(rs2)
            rs1 = instruction_line[1][:-1]

            remaining_string = instruction_line[2].replace("(", " ", 1)[:-1].split()
            rs2 = remaining_string[1]
        elif insn_subdict["Format"] == "U":
            # rd, imm
            rd = instruction_line[1][:-1]            
        elif insn_subdict["Format"] == "SB":
            # rs1, rs2, pc + imm
            rs1 = instruction_line[1][:-1]
            rs2 = instruction_line[2][:-1]
        elif insn_subdict["Format"] == "UJ":
            # pc + imm
            rd = "ra"
        elif insn_subdict["Format"] == "CR":     # Compressed formats
            # rs/d, rs
            if(insn_name=="c.jr" or insn_name=="c.jalr"):
                # rs
                rs1 = instruction_line[1][:-1]
            else:
                first_reg = instruction_line[1][:-1]
                rd = first_reg
                rs1 = instruction_line[2]

                # Cases where the destination register is also being read from
                if(insn_name=="c.add" or insn_name=="c.addw" or insn_name=="c.sub"):
                    rs2 = first_reg

        elif insn_subdict["Format"] == "CI":
            # rs/d, imm,
            first_reg = instruction_line[1][:-1]
            rd = first_reg

            if(insn_subdict["Type"] == "load"):
                # rd, imm(rs)
                remaining_string = instruction_line[2].replace("(", " ", 1)[:-1].split()
                rs1 = remaining_string[1]
            elif(insn_name == "c.addi" or insn_name == "c.addiw" or 
                insn_name == "c.addi16sp" or insn_name == "c.slli"):
                # Cases where the dest register is also read from
                rs1 = first_reg
        elif insn_subdict["Format"] == "CSS":
            # rs, imm(sp)
            rs1 = instruction_line[1][:-1]
            rs2 = "sp"
        elif insn_subdict["Format"] == "CIW":
            # rd, sp, imm
            rd = instruction_line[1][:-1]
            rs1 = "sp"
        elif insn_subdict["Format"] == "CL":
            # rd, imm(rs) - can merge with  'I'
            rd = instruction_line[1][:-1]
            remaining_string = instruction_line[2].replace("(", " ", 1)[:-1].split()
            rs1 = remaining_string[1]
        elif insn_subdict["Format"] == "CS":
            # rs1, imm(rs2) - can merge with 'S'
            rs1 = instruction_line[1][:-1]
            remaining_string = instruction_line[2].replace("(", " ", 1)[:-1].split()
            rs2 = remaining_string[1]
        elif insn_subdict["Format"] == "CA":
            pass # TODO
        elif insn_subdict["Format"] == "CB":
            # rs, pc + imm
            rs1 = instruction_line[1][:-1]
        elif insn_subdict["Format"] == "CJ":
            # pc + imm
            # TODO : Add specific case for 'jumpl' instruction types where
            #   the return address is added to the rd dictionary
            if(insn_name=="c.jal"):
                rd = "ra"
        else:
            pass # Do nothing if the column has nothing
        return rs1, rs2, rd
    # If the instruction isn't detected in the insn_pairs dictionary e.g. ret
    return "","",""
