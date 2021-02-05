#Calculate number of floor panels lengthwise
		panels_lengthwise = partobj.Length / 1219.2
		print ( "Panels lengthwise: "		, panels_lengthwise )
		print ( "Panels lengthwise: "		, math.ceil(panels_lengthwise) )

		#Calculate unmber of floor panels widthwise
		panels_widthwise = partobj.Width / 2438.40
		print ( "Panels widthwise: "		, panels_widthwise )
		print ( "Panels widthwise: "		, math.ceil(panels_widthwise) )

		#Calculate lengwise offset
		lw_offset = ( partobj.Width	% 1219.2 )
		print( "Lengthwise Offset: ", lw_offset.Value )	

		#Calculate widthwise offset.
		ww_offset = ( partobj.Length % 2438.4 )
		print( "Widthwise Offset: ", ww_offset.Value )		

		print( "Cut: ", 2438.4 - ww_offset.Value )

		current_panel = 0

		#Add panels
		for lw in range( 0, math.ceil( panels_lengthwise)  ):
			for ww in range( 0, math.ceil ( panels_widthwise ) ):
				names.append ( floorpanel.makePanel( "FloorPanel" ).Name )
		
				current_panel += 1

				print ( "Plate#: ", current_panel, "\tlw plates: ", math.ceil (panels_lengthwise), "\tMod lw: ", current_panel % math.ceil (panels_lengthwise),"\tMod ww: ",current_panel % math.ceil (panels_widthwise)   )

				lw_mod = current_panel % math.ceil (panels_lengthwise)
				ww_mod = current_panel % math.ceil (panels_widthwise)

				if( ( lw_mod == 3 ) and ( ww_mod == 0 ) ):
					lengths.append ( lw_offset.Value )					
					placement_offset = 	0
					print("cut panel")
				elif( ( lw_mod == 4 ) and ( ww_mod == 1 ) ):
					lengths.append ( lw_offset.Value )
					placement_offset = 	0
					print("cut panel")
				elif( ( lw_mod == 5 ) and ( ww_mod == 2 ) ):
					placement_offset = 2438.4 - lw_offset.Value
					print("shifted panel")
				elif( ( lw_mod == 0 ) and ( ww_mod == 0 ) ):
					placement_offset = 2438.4 - lw_offset.Value
					print("shifted panel")
				else:
					print("standard panel")
					lengths.append ( '2438.4 mm' )
					placement_offset = 	0

				#last in row			

				placements.append( FreeCAD.Vector ( 1219.2 * lw, (-2438.4 * ww + 88.90) + placement_offset  , -60.825)  )
				rotations.append (FreeCAD. Rotation ( 0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )
				#print( "lw = ",lw,"placement x: ", 1219.2 * lw ," placement y: ", 88.90 ) 

