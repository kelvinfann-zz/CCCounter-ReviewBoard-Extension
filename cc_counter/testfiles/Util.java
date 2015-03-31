
public final class Util {
	public static void exit(int i, String msg){
		System.out.println(msg);
		System.exit(i);
	}
	public static int[] strToInt(String s, int length, int exit){
		try{
			int[] rVal = breakString(s);
			if(rVal.length != length) System.exit(exit);
			return rVal;
		} catch(Exception e) {
			System.exit(exit); //incase we get nonnumeric inputs
		}
		exit(-1, "strToInt got to a point where it should have been impossible");
		return null; //should never get to this point
	}
	public static int[] breakString(String s){
		String[] temp = s.split("\\s+");
		int[] rVal = new int[temp.length];
		for(int i = 0; i < temp.length; i++){
			rVal[i] = Integer.parseInt(temp[i]);
		}
		return rVal;
	}
	public static boolean itemsLength(String s, int i, int exit){
		if(s.split("\\s+").length == i) return true;
		System.exit(exit);
		return false;
	}
}
